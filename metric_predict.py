import os
import pandas as pd

import torch
import transformers
import metricx.metricx24.models as models
from datasets import Dataset
from comet import download_model, load_from_checkpoint
from remedy.toolbox.score import (
    initialize_model, 
    load_translation_data,
    process_data_for_scoring,
    prepare_dataset,
    run_inference,
    calculate_scores,
    save_score_results,
    AutoTokenizer
)
from remedy.toolbox.languages import is_supported_language, get_supported_languages, LANG_MAP

class BasePredictor:
    def __init__(self, param_dict):
        raise NotImplementedError("BasePredictor is an abstract class and cannot be instantiated directly.")
    
    def predict(self, examples: list) -> list:
        raise NotImplementedError("Subclasses must implement the predict method.")
        


class MetricxPredictor(BasePredictor):

    def __init__(self, param_dict):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
    
        model_name_or_path = param_dict.get("model_name_or_path", "google/metricx-24-hybrid-xl-v2p6")
        tokenizer_name = param_dict.get("tokenizer", "google/mt5-xl")
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer_name)

        self.model = models.MT5ForRegression.from_pretrained(
        model_name_or_path, torch_dtype="auto")

        self.model.to(self.device)
        self.model.eval()
        self.training_args = transformers.TrainingArguments(
            output_dir=param_dict.get("output_dir", "./metrcx-24-results"),
            per_device_eval_batch_size=param_dict.get("batch_size", 1),
            dataloader_pin_memory=False,
        )
      

    def predict(self, set_of_examples: list):
        # Prepare the dataset for prediction
        # input: list of dicts with keys: "source", "hypothesis"
        tokenizer = self.tokenizer

        def _make_input(example):
            example["input"] = (
                "source: "
                + example["source"]
                + " candidate: "
                + example["hypothesis"]
            )
            return example

        def _tokenize(example):
            return tokenizer(
                example["input"],
                max_length=15376,
                truncation=True,
                padding=False,
            )

        def _remove_eos(example):
            example["input_ids"] = example["input_ids"][:-1]
            example["attention_mask"] = example["attention_mask"][:-1]
            return example


        ds = Dataset.from_list(set_of_examples)
        ds = ds.map(_make_input)
        ds = ds.map(_tokenize)
        ds = ds.map(_remove_eos)
        ds.set_format(
                type="torch",
                columns=["input_ids", "attention_mask"],
                device=self.device,
                output_all_columns=True,
            )
        
        trainer = transformers.Trainer(
            model=self.model,
            args=self.training_args,
        )
        results = []
        #predict for each hypothesis to get the pointwise scores
        predictions, _, _ = trainer.predict(test_dataset=ds)
        for pred, example in zip(predictions, ds):
            example["prediction"] = 5.0-float(pred)
            del example["input"]
            del example["input_ids"]
            del example["attention_mask"]
            results.append(example)
           
        return results

class CometQEPredictor(BasePredictor):
    def __init__(self, param_dict):
        # Choose your model from Hugging Face Hub
        model_path = download_model(param_dict.get("model_name_or_path", "Unbabel/wmt22-cometkiwi-da"))

        # Load the model checkpoint:
        self.model = load_from_checkpoint(model_path)
    
    def predict(self, examples: list) -> list:
        to_translate = [{"src": ex["source"], 
                     "mt": ex["hypothesis"], 
                     "ref": ex.get("reference", "")} for ex in examples]
    
        # Call predict method:
        model_output = self.model.predict(to_translate, batch_size=1, gpus=1)

        for example, score in zip(examples, model_output.scores):
            example["prediction"] = float(score)

        return examples

class RemedyQEPredictor(BasePredictor):
    #Adapted from https://github.com/Smu-Tan/Remedy/blob/main/remedy/toolbox/score.py
    def __init__(self, param_dict):
        self.llm = initialize_model(param_dict.get("model","ShaomuTan/ReMedy-2B"), 
                           param_dict.get("max_length",4096), 
                           param_dict.get("enable_truncate",False), 
                           param_dict.get("num_gpus",1), 
                           param_dict.get("num_seqs",256), 
                           param_dict.get("cache_dir", None),
                           param_dict.get("gpu_memory_utilization",0.3))
        self.tokenizer = AutoTokenizer.from_pretrained(param_dict.get("model","ShaomuTan/ReMedy-2B"), use_fast=True)
        self.calibrate = param_dict.get("calibrate", False)
        self.max_length = param_dict.get("max_length", 4096)
        # Extract metric name from model path
        metric_name = self.extract_model_name(param_dict.get("model","ShaomuTan/ReMedy-2B"))
        print(f"Using metric name: {metric_name}")
        self.enable_truncate = param_dict.get("enable_truncate", False)


    def extract_model_name(self, model_path):
        """Extract model name from path for use as metric name."""
        # Get the base directory name
        base_name = os.path.basename(os.path.normpath(model_path))
        
        # For HF model IDs like "ShaomuTan/ReMedy-9B-22", extract just the model name
        if '/' in base_name:
            return base_name.split('/')[-1]
        
        return base_name


    def predict(self, examples: list) -> list:
        df_data = self._load_df_from_list(examples)
        print("Processing data...")
        ds_data, df_data = process_data_for_scoring(df_data, QE=True)
        ds_data = prepare_dataset(ds_data, self.tokenizer, self.max_length, self.enable_truncate)

        print("Running inference...")
        embeddings = run_inference(self.llm, ds_data)
        if self.calibrate:
            print("Applying entropy-based calibration...")
            df_with_scores = calculate_scores(embeddings, df_data, calibrate=True)
        else:
            df_with_scores = calculate_scores(embeddings, df_data)
        
        # Convert DataFrame back to list of dicts
        results = []
        for example, score in zip(examples, df_with_scores['sigmoid:seg']):
            example["prediction"] = float(score)
            results.append(example)
        return results
    
    @staticmethod
    def _load_df_from_list(examples: list):
        # Create language pair
        lp = f"{examples[0]['src_lang']}-{examples[0]['tgt_lang']}"
        
        src_lines = [ex['source'] for ex in examples]
        mt_lines = [ex['hypothesis'] for ex in examples]
        # Create DataFrame
        data_dict = {
            'src': src_lines,
            'mt': mt_lines,
            'lp': [lp] * len(src_lines),
            'seg_id': list(range(len(src_lines))),
            'system-name': ['custom_system'] * len(src_lines),
            'human_ratings': [0.0] * len(src_lines)  # Dummy ratings since we don't have them
        }
        
        data_dict['ref'] = [''] * len(src_lines)  # Empty refs for QE mode
        
        df = pd.DataFrame.from_dict(data_dict)
        
        return df
                                            