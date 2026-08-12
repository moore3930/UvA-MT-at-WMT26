# WMT26 Required-Only Instruction Report

Source file: `wmt26_genmt_required_only.jsonl`
Rows: `14969`
Languages: `30`

## Cluster Summary

- `simple_code_direction`: `7006` rows, `8` unique instructions. Minimal code-based prompts like "Translate from en to xx".
- `professional_translator_spoken_asr`: `2983` rows, `20` unique instructions. Professional translator prompt for ASR-like spoken transcripts, preserving colloquial flow and sentence-per-line output.
- `inclusive_gender_slash_formatting`: `2000` rows, `2` unique instructions. English->Slavic prompt requiring gender-inclusive slash forms such as купил/а or rád/a.
- `professional_translator_social_media`: `1103` rows, `20` unique instructions. Professional translator prompt for social-media text, with hashtag/URL handling and informal style.
- `professional_translator_news_html`: `489` rows, `20` unique instructions. Professional translator prompt for news articles with formal journalistic style and HTML preservation.
- `legal_it_to_de_with_term_constraints`: `485` rows, `466` unique instructions. Italian->German legal translation prompts with jurisdiction-specific terminology constraints and candidate term choices.
- `simple_named_direction`: `345` rows, `1` unique instructions. Minimal named-language prompts like "Translate from English to Faroese/Icelandic".
- `wesnoth_dialogue_persona_conditioned`: `236` rows, `50` unique instructions. English->Korean game-dialogue prompts conditioned on character persona, status, and speech act.
- `professional_translator_czech_education_html`: `189` rows, `3` unique instructions. Professional translator prompt for Czech school exercises in biology/chemistry/geography, preserving HTML.
- `professional_translator_software_json`: `133` rows, `19` unique instructions. Professional translator prompt for software JSON, preserving keys/placeholders and valid JSON structure.

## Per-Language Inventory

### `arz`
- Rows: `150`
- Unique instructions: `1`
- Instruction clusters: `simple_code_direction` x 1

1. `150` rows | `simple_code_direction`
   Translate from en to arz.

   Raw instruction:

   ```text
   Translate from en to arz.
   ```

### `arz_Arab`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Arabic, Egyptian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Arabic, Egyptian translator, tasked with providing translations suitable for use in Arabic, Egyptian (arz_Arab). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Arabic, Egyptian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Arabic, Egyptian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Arabic, Egyptian (arz_Arab):
   ```

2. `44` rows | `professional_translator_social_media`
   Arabic, Egyptian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Arabic, Egyptian translator, tasked with providing translations suitable for use in Arabic, Egyptian (arz_Arab). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Arabic, Egyptian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Arabic, Egyptian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Arabic, Egyptian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Arabic, Egyptian (arz_Arab):
   ```

3. `14` rows | `professional_translator_news_html`
   Arabic, Egyptian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Arabic, Egyptian translator, tasked with providing translations suitable for use in Arabic, Egyptian (arz_Arab). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Arabic, Egyptian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Arabic, Egyptian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Arabic, Egyptian (arz_Arab):
   ```

4. `7` rows | `professional_translator_software_json`
   Arabic, Egyptian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Arabic, Egyptian translator, tasked with providing translations suitable for use in Arabic, Egyptian (arz_Arab). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Arabic, Egyptian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Arabic, Egyptian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Arabic, Egyptian (arz_Arab):
   ```

### `bel_Cyrl`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Belarusian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Belarusian translator, tasked with providing translations suitable for use in Belarusian (bel_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Belarusian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Belarusian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Belarusian (bel_Cyrl):
   ```

2. `44` rows | `professional_translator_social_media`
   Belarusian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Belarusian translator, tasked with providing translations suitable for use in Belarusian (bel_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Belarusian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Belarusian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Belarusian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Belarusian (bel_Cyrl):
   ```

3. `14` rows | `professional_translator_news_html`
   Belarusian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Belarusian translator, tasked with providing translations suitable for use in Belarusian (bel_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Belarusian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Belarusian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Belarusian (bel_Cyrl):
   ```

4. `7` rows | `professional_translator_software_json`
   Belarusian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Belarusian translator, tasked with providing translations suitable for use in Belarusian (bel_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Belarusian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Belarusian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Belarusian (bel_Cyrl):
   ```

### `ces_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Czech: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Czech translator, tasked with providing translations suitable for use in Czech (ces_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Czech grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Czech translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Czech (ces_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Czech: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Czech translator, tasked with providing translations suitable for use in Czech (ces_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Czech grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Czech. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Czech translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Czech (ces_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Czech: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Czech translator, tasked with providing translations suitable for use in Czech (ces_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Czech grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Czech translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Czech (ces_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Czech: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Czech translator, tasked with providing translations suitable for use in Czech (ces_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Czech grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Czech translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Czech (ces_Latn):
   ```

### `cs`
- Rows: `1050`
- Unique instructions: `2`
- Instruction clusters: `inclusive_gender_slash_formatting` x 1, `simple_code_direction` x 1

1. `1000` rows | `inclusive_gender_slash_formatting`
   Czech: gender-inclusive slash forms required for past participles/adjectives; no extra output.

   Raw instruction:

   ```text
   Translate the English text into Czech. Make the gender of the author inclusive by combining both masculine and feminine endings using slashes.
    
    Follow these formatting rules strictly:
    use the slash to separate the masculine and feminine endings 
    1. for past tense verb participles, e.g., "koupil/a", "napsal/a" 
    2. for adjectives, e.g., "rád/a", "naštvaný/á", "veselý/á" 
   
    Only output the translation, with no additional formatting or explanations.  
   
    Example 1: "I am happy that I bought it" -> "Jsem rád/a, že jsem to koupil/a" 
    Example 2: "I never saw or heard it" -> "Nikdy jsem to neviděl/a ani neslyšel/a" 
   
    TEXT: 
   ```

2. `50` rows | `simple_code_direction`
   Translate from en to cs.

   Raw instruction:

   ```text
   Translate from en to cs.
   ```

### `cs_CZ`
- Rows: `917`
- Unique instructions: `1`
- Instruction clusters: `simple_code_direction` x 1

1. `917` rows | `simple_code_direction`
   Translate from en to cs_CZ.

   Raw instruction:

   ```text
   Translate from en to cs_CZ.
   ```

### `de_DE`
- Rows: `2149`
- Unique instructions: `467`
- Instruction clusters: `legal_it_to_de_with_term_constraints` x 466, `simple_code_direction` x 1

1. `1664` rows | `simple_code_direction`
   Translate from en to de_DE.

   Raw instruction:

   ```text
   Translate from en to de_DE.
   ```

2. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'giurisdizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'giurisdizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtsprechung
   2. Gerichtsbarkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

3. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'focolaio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'focolaio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ausbruch
   2. Ausbruchsgebiet
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

4. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'scala'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'scala' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Treppe
   2. Treppenhaus
   3. Leiter
   4. Treppenraum
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

5. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'segnale di prescrizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'segnale di prescrizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gebotszeichen
   2. Vorschriftszeichen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

6. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'gradino'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'gradino' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Stufe
   2. Treppenstufe
   3. Leiterstufe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

7. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rifiuto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rifiuto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Abfall
   2. Verweigerung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

8. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'esigibilità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'esigibilità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Fälligkeit
   2. Zumutbarkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

9. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'servitù'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'servitù' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Grunddienstbarkeit
   2. Dienstbarkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

10. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'provvedimento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'provvedimento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwaltungsakt
   2. Maßnahme
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

11. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'impugnazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'impugnazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Anfechtung
   2. Rechtsmittel
   3. Rechtsmittelverfahren
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

12. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'emittente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'emittente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Veranstalter
   2. Aussteller
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

13. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'obbligo di comunicazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'obbligo di comunicazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Informationspflicht
   2. Mitteilungspflicht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

14. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'società di capitali'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'società di capitali' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gründungsgesellschaft
   2. Kapitalgesellschaft
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

15. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'convivenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'convivenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zusammenleben
   2. eheliche Lebensgemeinschaft
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

16. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'espropriazione presso terzi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'espropriazione presso terzi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zwangsvollstreckung in Geldforderungen
   2. Zwangsvollstreckung in Forderungen und andere Vermögensrechte
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

17. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autonomia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autonomia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtsetzungskompetenz
   2. Selbstverwaltung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

18. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'trasmissione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'trasmissione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Übertragung
   2. Übermittlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

19. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'vizio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'vizio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mangel
   2. Fehler
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

20. `2` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pubblicità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pubblicità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Publizität
   2. Werbung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

21. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'banchina'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'banchina' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Straße
   2. Seitenstreifen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

22. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'arresto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'arresto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Festnahme
   2. Freiheitsstrafe
   3. Verhaftung
   4. Warten
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

23. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'archivio di deposito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'archivio di deposito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zwischenarchiv
   2. Verwaltungsarchiv
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

24. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione delle mani'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione delle mani' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutz der Hände
   2. Handschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

25. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto preparatorio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto preparatorio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. vorbereitende Verfahrenshandlung
   2. Vorbereitungshandlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

26. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ipoacusia da rumore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ipoacusia da rumore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lärmschwerhörigkeit
   2. lärmbedingte Hörschädigung
   3. lärmbedingter Gehörschaden
   4. lärmbedingte Schädigung
   5. Lärmschaden
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

27. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto procedimentale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto procedimentale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verfahrenshandlung
   2. Verfahrensakt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

28. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'interpretazione logico-sistematica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'interpretazione logico-sistematica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. systematische Interpretation
   2. logisch-systematische Auslegung
   3. logisch-systematische Interpretation
   4. logische Interpretation
   5. systematische Auslegung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

29. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fatto illecito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fatto illecito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. unerlaubte Handlung
   2. rechtswidrige Handlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

30. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dolo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dolo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. arglistige Täuschung
   2. Vorsatz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

31. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'linea elettrica aerea a media tensione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'linea elettrica aerea a media tensione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hochspannungsfreileitung
   2. Mittelspannungsfreileitung
   3. Niederspannungsfreileitung
   4. Freileitung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

32. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto processuale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto processuale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktenstück
   2. Verfahrenshandlung
   3. Prozesshandlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

33. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'obbligo di motivazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'obbligo di motivazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Begründungszwang
   2. Begründungspflicht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

34. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'codice di identificazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'codice di identificazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kennnummer
   2. Benutzerkennung
   3. Kennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

35. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'committente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'committente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geschäftsherr
   2. Bauherr
   3. Versender
   4. Dienstberechtigter
   5. Auftraggeber
   6. Kommittent
   7. Besteller
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

36. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'servizio di radiodiffusione di contenuti'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'servizio di radiodiffusione di contenuti' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rundfunkdienst
   2. Rundfunk
   3. Rundfunkinhaltedienst
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

37. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'circuito a bassissima tensione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'circuito a bassissima tensione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. FELV-Stromkreis
   2. ELV-Stromkreis
   3. SELV-Stromkreis
   4. PELV-Stromkreis
   5. Kleinspannungsstromkreis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

38. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'annullabilità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'annullabilità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aufhebbarkeit
   2. Vernichtbarkeit
   3. Anfechtbarkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

39. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fornitore di servizi di comunicazione elettronica accessibili al pubblico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fornitore di servizi di comunicazione elettronica accessibili al pubblico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Anbieter von öffentlich zugänglichen Telekommunikationsdiensten
   2. Anbieter eines öffentlich zugänglichen Telekommunikationsdienstes
   3. Anbieter des Dienstes
   4. Diensteanbieter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

40. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'matrimonio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'matrimonio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Trauung
   2. Ehe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

41. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'RR'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'RR' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wiederholungsverordnung
   2. Verschreibung zur wiederholten Abgabe
   3. VS-Vertraulich
   4. Wiederholungsrezept
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

42. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'conservazione dei beni culturali'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'conservazione dei beni culturali' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Konservierung
   2. Denkmalpflege
   3. Denkmalschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

43. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fatto illecito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fatto illecito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. rechtswidrige Handlung
   2. Delikt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

44. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'obbligazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'obbligazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schuldverschreibung
   2. Verpflichtung
   3. Verbindlichkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

45. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'scala estensibile'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'scala estensibile' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mehrzweckleiter
   2. Stehleiter mit aufgesetzter Schiebeleiter
   3. Mehrzweckleiter mit Gelenken
   4. tragbare Leiter
   5. Sprossenleiter
   6. dreiteilige Mehrzweckleiter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

46. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'conservazione dei beni culturali'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'conservazione dei beni culturali' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. präventive Konservierung
   2. Denkmalschutz
   3. Restaurierung
   4. Kulturgutschutz
   5. passive Konservierung
   6. vorbeugende Konservierung
   7. Konservierung
   8. Verhütung
   9. Denkmalpflege
   10. Prävention
   11. Vorbeugung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

47. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'revoca'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'revoca' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Widerruf
   2. Abberufung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

48. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'committente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'committente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geschäftsherr
   2. Besteller
   3. Versender
   4. Kommittent
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

49. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'termine'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'termine' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. prozessuale Frist
   2. Verfahrensfrist
   3. Termin
   4. Grenzzeichen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

50. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'esecuzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'esecuzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Durchführung
   2. Vollstreckung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

51. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'circuito FELV'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'circuito FELV' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. FELV-Stromkreis
   2. Kleinspannungsstromkreis
   3. PELV-Stromkreis
   4. SELV-Stromkreis
   5. ELV-Stromkreis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

52. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assicuratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assicuratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versicherungsvertreter
   2. Versicherungsunternehmen
   3. Versicherer
   4. Versicherungsgesellschaft
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

53. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'deliberazione della sentenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'deliberazione della sentenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Fällung des Urteils
   2. Beratung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

54. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'elettorato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'elettorato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wählerschaft
   2. Wahlrecht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

55. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'continua comunicazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'continua comunicazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ruf- und Sichtverbindung
   2. ständige Verbindung
   3. Verbindung über andere Mittel
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

56. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'deliberazione della sentenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'deliberazione della sentenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Beratung
   2. Urteilsfällung
   3. Fällung des Urteils
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

57. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'richiamo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'richiamo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ermahnung
   2. Impfauffrischung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

58. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lavoro minorile'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lavoro minorile' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeit
   2. Kinderarbeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

59. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione contro i contatti diretti'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione contro i contatti diretti' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutz bei indirektem Berühren
   2. Basisschutz
   3. Schutz gegen direktes Berühren
   4. Fehlerschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

60. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ricorso in opposizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ricorso in opposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Einspruch
   2. Aufsichtsbeschwerde
   3. Widerspruch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

61. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'targa provvisoria'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'targa provvisoria' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Nummernschild
   2. Ausfuhrkennzeichen
   3. rotes Kennzeichen
   4. amtliches Kennzeichen
   5. 5-Tages-Kennzeichen
   6. Kennzeichen
   7. Überführungskennzeichen
   8. internationales Kurzzeitkennzeichen
   9. Kurzzeitkennzeichen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

62. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'apparecchio di classe I'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'apparecchio di classe I' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gerät der Schutzklasse III
   2. Elektrogerät
   3. Gerät der Schutzklasse II
   4. schutzisoliertes Gerät
   5. Gerät der Schutzklasse I
   6. elektrisches Gerät
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

63. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'funzione amministrativa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'funzione amministrativa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwaltungsfunktion
   2. Verwaltungstätigkeit
   3. Verwaltungsaufgabe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

64. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'impianto di rivelazione automatica d'incendio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. automatische Brandmeldeanlage
   2. Löschanlage
   3. Brandschutzanlage
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

65. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispensa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispensa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ausnahmebewilligung
   2. Befreiung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

66. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'servizio di radiodiffusione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'servizio di radiodiffusione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rundfunk
   2. Funkdienst
   3. Rundfunkdienst
   4. Rundfunkinhaltedienst
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

67. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rischio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rischio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gefahr
   2. Risiko
   3. Gefährdung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

68. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'illecito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'illecito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Unrecht
   2. rechtswidriges Verhalten
   3. unerlaubte Handlung
   4. unerlaubt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

69. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tempo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tempo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zeitpunkt
   2. Zeitraum
   3. Zeit
   4. Dauer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

70. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tempo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tempo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Dauer
   2. Zeitpunkt
   3. Zeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

71. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'motivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'motivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Motiv
   2. Beweggrund
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

72. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispositivo anticaduta di tipo retrattile'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispositivo anticaduta di tipo retrattile' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Auffangsystem
   2. Höhensicherungsgerät
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

73. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'contraente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'contraente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vertragspartei
   2. Teilnehmer
   3. Partei
   4. Versicherungsnehmer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

74. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispositivo di sicurezza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispositivo di sicurezza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. nicht trennende Schutzeinrichtung
   2. Sicherheitsvorrichtung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

75. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'diritto di voto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'diritto di voto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wahlrecht
   2. Stimmrecht
   3. Aktienstimmrecht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

76. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'aggiornamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'aggiornamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktualisierung
   2. dienstliche Fortbildung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

77. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ordine pubblico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ordine pubblico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. öffentlicher Frieden
   2. öffentliche Ordnung
   3. öffentliche Sicherheit
   4. ordre public
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

78. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'codice di identificazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'codice di identificazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kennung
   2. Kennziffer
   3. Benutzerkennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

79. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'nuovo produttore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'nuovo produttore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ersterzeuger
   2. Abfallerzeuger
   3. Zweiterzeuger
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

80. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lesione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lesione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verletzung
   2. Angriff
   3. Verstoß
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

81. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autotreno'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autotreno' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lastzug
   2. Fahrzeug
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

82. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fondo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fondo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Fonds
   2. Grundstück
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

83. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'responsabilità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'responsabilità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verantwortung
   2. Verantwortlichkeit
   3. strafrechtliche Verantwortlichkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

84. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'IR'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'IR' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. ionisierende Strahlung
   2. IR-Strahlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

85. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'parte sotto tensione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'parte sotto tensione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. unter Spannung stehendes Teil
   2. unter Spannung stehendes aktives Teil
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

86. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione delle braccia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione delle braccia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutz der Arme
   2. Armschutzausrüstung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

87. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'società incorporante'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'società incorporante' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. neuer Rechtsträger
   2. übernehmender Rechtsträger
   3. übernehmende Gesellschaft
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

88. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fase di estinzione e raffreddamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fase di estinzione e raffreddamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Entstehungsphase
   2. Brandverlauf
   3. Abklingen
   4. Anfangsphase des Brandes
   5. voll entwickelter Brand
   6. Entstehungsbrandphase
   7. Abklingphase
   8. Vollbrand
   9. Zündphase
   10. Vollbrandphase
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

89. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'mutageno'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'mutageno' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. erbgutverändernder Stoff
   2. erbgutverändernd
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

90. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autonomia funzionale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autonomia funzionale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Träger funktionaler Selbstverwaltung
   2. funktionale Selbstverwaltungskörperschaft
   3. funktionale Selbstverwaltung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

91. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'giustizia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'giustizia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gerechtigkeit
   2. Justiz
   3. Rechtspflege
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

92. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'matrimonio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'matrimonio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ehe
   2. Heirat
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

93. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'buona fede'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'buona fede' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Treu und Glauben
   2. guter Glaube
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

94. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispositivo di sicurezza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispositivo di sicurezza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sicherheitseinrichtung
   2. nicht trennende Schutzeinrichtung
   3. Sicherheitsvorrichtung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

95. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'colpevolezza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'colpevolezza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vertretenmüssen
   2. Schuld
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

96. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'didattica in presenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'didattica in presenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. digitaler Unterricht
   2. Homeschooling
   3. Präsenzunterricht
   4. Distanzunterricht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

97. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'codice di identificazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'codice di identificazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Identifikationsnummer
   2. Benutzerkennung
   3. Kennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

98. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'svalutazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'svalutazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geldentwertung
   2. Abwertung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

99. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lista elettorale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lista elettorale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wahlvorschlagliste
   2. Wahlvorschlagsliste
   3. Verzeichnis der Wahlberechtigten
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

100. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'candidato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'candidato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Bewerber
   2. Wahlbewerber
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

101. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'commesso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'commesso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Handlungsgehilfe
   2. Verrichtungsgehilfe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

102. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pubblicazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pubblicazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verkündung
   2. Veröffentlichung
   3. Aufgebot
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

103. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione contro i contatti indiretti'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione contro i contatti indiretti' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutz bei indirektem Berühren
   2. Fehlerschutz
   3. Basisschutz
   4. Schutz gegen direktes Berühren
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

104. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'requisiti fisici e psichici'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'requisiti fisici e psichici' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. körperliche und geistige Anforderungen
   2. Anforderungen an das Sehvermögen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

105. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'principio di pubblicità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'principio di pubblicità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Öffentlichkeitsmaxime
   2. Öffentlichkeitsprinzip
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

106. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'archivio corrente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'archivio corrente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. laufende Registratur
   2. laufendes Archiv
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

107. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione dei capelli'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione dei capelli' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Haarschutz
   2. Schutz der Haare
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

108. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ambiente severo freddo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ambiente severo freddo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kältebereich
   2. warme Umgebung
   3. heiße Umgebung
   4. Kälteumgebung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

109. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'censura'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'censura' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zensur
   2. Verweis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

110. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'riconoscimento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'riconoscimento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Identifizierung
   2. Anerkennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

111. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'termine'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'termine' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. prozessuale Frist
   2. Verfahrensfrist
   3. Frist
   4. Grenzzeichen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

112. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'incorporazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'incorporazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verbindung
   2. Aufnahme
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

113. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'invenzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'invenzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erfindung
   2. Eigentumserwerb des Finders
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

114. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'committente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'committente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geschäftsherr
   2. Versender
   3. Dienstberechtigter
   4. Kommittent
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

115. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'misura di protezione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'misura di protezione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sicherheitsmaßnahme
   2. Maßregel der Besserung und Sicherung
   3. Schutzmaßnahme
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

116. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sistema SELV'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sistema SELV' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. SELV-System
   2. FELV-System
   3. PELV-System
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

117. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sicuro allo sfondamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sicuro allo sfondamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. begehbar
   2. betretbar
   3. bedingt begehbar
   4. nicht durchsturzsicher
   5. durchsturzsicher
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

118. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'cosa comune'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'cosa comune' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gemeingut
   2. gemeinschaftliche Sache
   3. gemeinschaftlicher Gegenstand
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

119. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'impossessamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'impossessamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zueignung
   2. Besitzergreifung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

120. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'mediazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'mediazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mediation
   2. Maklervertrag
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

121. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'precedenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'precedenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vorrang
   2. Vorfahrt
   3. Vorzug
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

122. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'specificazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'specificazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verarbeitung
   2. Konkretisierung
   3. Konzentration
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

123. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'riserva'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'riserva' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Pflichtteil
   2. Rücklage
   3. Vorbehalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

124. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'doccia di sicurezza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'doccia di sicurezza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Notdusche
   2. Erste-Hilfe-Ausstattung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

125. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'delega'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'delega' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Bevollmächtigung
   2. Übertragung von Befugnissen
   3. Vollmachtsurkunde
   4. Vollmacht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

126. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'libretto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'libretto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sparbuch
   2. Zulassungsbescheinigung Teil I
   3. Zulassungsbescheinigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

127. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'intensità dell'esposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Expositionsdauer
   2. Exposition
   3. Einwirkungsdauer
   4. Expositionsart
   5. Expositionsintensität
   6. Expositionswert
   7. Expositionsausmaß
   8. Einwirkdauer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

128. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'recupero'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'recupero' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rehabilitation
   2. Verwertung
   3. Suchtrehabilitation
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

129. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'radiazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'radiazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Abmeldung
   2. Außerbetriebssetzung
   3. Abmeldebescheinigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

130. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sistema FELV'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sistema FELV' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. PELV-System
   2. SELV-System
   3. FELV-System
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

131. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'DL'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'DL' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. DL
   2. Bauleiter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

132. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto normativo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto normativo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtsverordnung
   2. Verfassung
   3. Errichtung
   4. Gründung
   5. Gesellschaftsvertrag
   6. Statut
   7. Rechtsetzungsakt
   8. Gesellschaftsgründung
   9. Gesetz
   10. Geschäftsordnung
   11. Rechtshandlung
   12. Verordnung
   13. formelles Gesetz
   14. Satzung
   15. G
   16. juristische Handlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

133. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'procuratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'procuratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Prozessbevollmächtigter
   2. Prokurist
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

134. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lettura'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lettura' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verlesung
   2. Lesung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

135. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'promittente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'promittente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versprechender
   2. Verlobter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

136. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto materiale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto materiale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Tathandlung
   2. Realakt
   3. schlicht-hoheitliches Verwaltungshandeln
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

137. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'aggiornamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'aggiornamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktualisierung
   2. Fortbildung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

138. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'massa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'massa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. fremdes leitfähiges Teil
   2. Körper
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

139. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'CAP'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'CAP' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Postleitzahl
   2. Fahrerlaubnis zur Fahrgastbeförderung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

140. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'maschera con filtro intercambiabile'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'maschera con filtro intercambiabile' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vollmaske mit austauschbarem Filter
   2. Atemschutzmaske mit austauschbarem Filter
   3. Halbmaske mit austauschbarem Filter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

141. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'mezzo di salvataggio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'mezzo di salvataggio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. PSA
   2. Schutzausrüstung
   3. Rettungsmittel
   4. persönliche Schutzausrüstung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

142. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'segreto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'segreto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. geheim
   2. geh.
   3. Geheimhaltung
   4. Geheimnis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

143. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fondatore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fondatore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gründer
   2. Stifter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

144. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sostituito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sostituito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ersatzerbe
   2. Nacherbe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

145. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'associato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'associato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. stiller Gesellschafter
   2. Stiller
   3. still Beteiligter
   4. Mitglied
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

146. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'causa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'causa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. causa
   2. Rechtsgrund
   3. Rechtsstreit
   4. Ursache
   5. Streitsache
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

147. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lista elettorale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lista elettorale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verzeichnis der Wahlberechtigten
   2. Wählerverzeichnis
   3. Wahlvorschlagsliste
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

148. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'comando'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'comando' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gebot
   2. Abordnung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

149. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'causa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'causa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ursache
   2. Rechtsstreit
   3. Streitsache
   4. Rechtsgrund
   5. causa
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

150. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'penale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'penale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vertragsstrafe
   2. strafrechtlich
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

151. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'esplosivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'esplosivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. explosionsgefährlich
   2. explosionsfähig
   3. explosiv
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

152. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'agente biologico del gruppo 1'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'agente biologico del gruppo 1' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Biostoff der Risikogruppe 3
   2. Biostoff
   3. Biostoff der Risikogruppe 1
   4. Biostoff der Risikogruppe 2
   5. Biostoff der Risikogruppe 4
   6. biologischer Arbeitsstoff
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

153. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'apparecchio di classe III'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'apparecchio di classe III' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gerät der Schutzklasse III
   2. Elektrogerät
   3. elektrisches Gerät
   4. Gerät der Schutzklasse I
   5. Gerät der Schutzklasse II
   6. schutzisoliertes Gerät
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

154. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pericolo di inalazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pericolo di inalazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gefahr
   2. Einatmungsgefahr
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

155. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'aggiornamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'aggiornamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. berufliche Weiterbildung
   2. Aktualisierung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

156. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispositivo di sicurezza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispositivo di sicurezza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sicherheitseinrichtung
   2. nicht trennende Schutzeinrichtung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

157. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'trasporto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'trasporto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Frachtvertrag
   2. Beförderung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

158. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'periodo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'periodo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zeitraum
   2. Satz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

159. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'funzione amministrativa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'funzione amministrativa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwaltungsaufgabe
   2. Verwaltungstätigkeit
   3. Verwaltung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

160. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'obbligo di informazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'obbligo di informazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erkundigungspflicht
   2. Informationspflicht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

161. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'scala'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'scala' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Leiter
   2. Treppe
   3. Treppenhaus
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

162. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rumore di fondo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rumore di fondo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hintergrundlärm
   2. Lärm
   3. Geräusch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

163. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'codice identificativo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'codice identificativo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kennung
   2. Passwort
   3. Benutzerkennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

164. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'effetti diretti'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'effetti diretti' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. unmittelbare Auswirkungen
   2. mittelbare Auswirkungen
   3. direkte Auswirkungen
   4. unmittelbare Wirkungen
   5. chronische Wirkungen
   6. indirekte Auswirkungen
   7. akute Wirkungen
   8. mittelbare Wirkungen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

165. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'amministratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'amministratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwalter
   2. Mitglied des Vorstandes
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

166. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'conservazione dei beni culturali'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'conservazione dei beni culturali' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Konservierung
   2. Denkmalschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

167. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fermata'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fermata' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Halten
   2. Haltestelle
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

168. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pericolo per la salute'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pericolo per la salute' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gesundheitsgefahr
   2. Umweltgefahr
   3. physikalische Gefahr
   4. Gefahr
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

169. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'duplicato della patente di guida'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'duplicato della patente di guida' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ersatzführerschein
   2. Führerschein
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

170. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'accesso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'accesso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zugangsrecht
   2. Zutritt
   3. Zugangsöffnung
   4. Zugang
   5. Zufahrt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

171. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'istruttoria'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'istruttoria' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vorbereitung der Entscheidung
   2. Sachverhaltsermittlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

172. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'contraente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'contraente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vertragspartei
   2. Teilnehmer
   3. Versicherungsnehmer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

173. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'seggio elettorale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'seggio elettorale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wahllokal
   2. Wahlraum
   3. Wahlvorstand
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

174. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'estinzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'estinzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aussterben
   2. Erlöschen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

175. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'obbligazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'obbligazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schuldverschreibung
   2. Verbindlichkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

176. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'consulenza tecnica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'consulenza tecnica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sachverständigengutachten
   2. Gerichtsgutachten
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

177. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'emissione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'emissione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Begebung
   2. Schadstoffemissionen
   3. Emissionen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

178. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lista elettorale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lista elettorale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wählerverzeichnis
   2. Wahlvorschlagsliste
   3. Wahlvorschlagliste
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

179. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rischio di trascinamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rischio di trascinamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Einzugsrisiko
   2. Risiko
   3. Gefahr
   4. Quetschrisiko
   5. Quetschgefährdung
   6. Gefährdung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

180. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'relazione degli amministratori'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'relazione degli amministratori' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verschmelzungsbericht
   2. Lagebericht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

181. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto processuale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto processuale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktenteil
   2. Aktenstück
   3. Prozesshandlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

182. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fondatore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fondatore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gründungsaktionär
   2. Stifter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

183. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'domanda'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'domanda' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gesuch
   2. Anspruch
   3. Antrag
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

184. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'società incorporante'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'società incorporante' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. übernehmender Rechtsträger
   2. neuer Rechtsträger
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

185. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tolleranza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tolleranza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Duldung
   2. Toleranz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

186. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rischio di caduta dall'alto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Absturzgefährdung
   2. Sturzgefährdung
   3. Sturzrisiko
   4. Sturz- und Absturzrisiko
   5. Absturzrisiko
   6. Sturz- und Absturzgefährdung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

187. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pittogramma'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pittogramma' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gefahrenpiktogramm
   2. graphisches Symbol
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

188. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'agente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'agente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeitsstoff
   2. Täter
   3. Einwirkung
   4. Handelsvertreter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

189. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tasso alcolemico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tasso alcolemico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. AAK
   2. Atemalkoholkonzentration
   3. Blutalkoholgehalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

190. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'cintura di trattenuta'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'cintura di trattenuta' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rückhaltegurt
   2. Haltegurt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

191. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'funzione amministrativa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'funzione amministrativa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwaltungstätigkeit
   2. Verwaltung
   3. Verwaltungsfunktion
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

192. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'segreto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'segreto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geheimhaltung
   2. geheim
   3. Geheimnis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

193. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'partecipante'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'partecipante' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Teilhaber
   2. Teilnehmer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

194. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'archivio di deposito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'archivio di deposito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zwischenarchiv
   2. Altregistratur
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

195. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'custodia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'custodia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aufbewahrung
   2. Obhut
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

196. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'infortunio domestico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'infortunio domestico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Unfall
   2. Haushaltsunfall
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

197. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'emissione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'emissione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schadstoffemissionen
   2. Begebung
   3. Emission
   4. Ausgabe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

198. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'conservazione del paesaggio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'conservazione del paesaggio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Landschaftspflege
   2. Landschaftsschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

199. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtshandlung
   2. Handlung
   3. Urkunde
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

200. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'diritto di voto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'diritto di voto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktienstimmrecht
   2. Wahlrecht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

201. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'utensile manuale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'utensile manuale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. handgehaltenes Werkzeug
   2. Handwerkzeug
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

202. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'efficacia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'efficacia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Werbung
   2. Offenkundigkeit
   3. Zügigkeit
   4. Wirtschaftlichkeit
   5. Publizität
   6. Effizienz
   7. Effektivität
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

203. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tronco di sostegno'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tronco di sostegno' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Stützschenkel
   2. Stehleiter
   3. Steigschenkel
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

204. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assicuratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assicuratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versicherungsunternehmen
   2. Versicherungsvertreter
   3. Versicherungsagent
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

205. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'libretto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'libretto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sparbuch
   2. Zulassungsbescheinigung Teil I
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

206. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rumore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rumore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lärm
   2. Geräusch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

207. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'annullabilità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'annullabilità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aufhebbarkeit
   2. Vernichtbarkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

208. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'regolamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'regolamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verordnung
   2. Geschäftsordnung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

209. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'estinzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'estinzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erlöschen
   2. Aussterben
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

210. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sviluppo dell'incendio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Brandverlauf
   2. Brandausbreitung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

211. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'bene'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'bene' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gut
   2. Produktionsgut
   3. Investitionsgut
   4. Kapitalgut
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

212. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'eccesso di potere'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'eccesso di potere' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Überschreitung der Vertretungsmacht
   2. Ermessensfehler
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

213. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'possesso di mala fede'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'possesso di mala fede' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. redlicher Besitz
   2. unredlicher Besitz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

214. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ripartizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ripartizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Abteilung
   2. Aufteilung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

215. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'consenso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'consenso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zustimmung
   2. Konsens
   3. Einwilligung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

216. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'organo monocratico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'organo monocratico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. monokratisch organisierte Behörde
   2. Organ
   3. Kollegialorgan
   4. Kollegialbehörde
   5. monokratisch strukturierte Behörde
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

217. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tutela'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tutela' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vormundschaft
   2. Wahrung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

218. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'convivente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'convivente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lebensgefährte
   2. im Haushalt lebende Person
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

219. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'IR'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'IR' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. ionisierende Strahlung
   2. IR
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

220. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'legale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'legale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. gesetzesmäßig
   2. rechtsgültig
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

221. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'falso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'falso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. falsch
   2. Fälschung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

222. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ponte su ruote a torre'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ponte su ruote a torre' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. mobiles Gerüst
   2. fahrbares Gerüst
   3. Rollgerüst
   4. Fahrgerüst
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

223. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assemblea'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assemblea' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hauptversammlung
   2. Gesellschafterversammlung
   3. Mitgliederversammlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

224. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'flacone lavaocchi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'flacone lavaocchi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Augendusche
   2. Augennotdusche
   3. Augenspüleinrichtung
   4. Augenspülflasche
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

225. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'precedenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'precedenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vorfahrt
   2. Vorzug
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

226. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'contraente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'contraente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versicherungsnehmer
   2. Partei
   3. Vertragspartei
   4. Teilnehmer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

227. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'distanza sociale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'distanza sociale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Abstand
   2. räumliche Distanz
   3. soziale Distanz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

228. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Urkunde
   2. Handlung
   3. Rechtshandlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

229. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'seggio elettorale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'seggio elettorale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wahlvorstand
   2. Wahllokal
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

230. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'capacità lavorativa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'capacità lavorativa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erwerbsfähigkeit
   2. Arbeitsfähigkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

231. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'cosa comune'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'cosa comune' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. gemeinschaftliche Sache
   2. Gemeingut
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

232. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'termine'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'termine' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Frist
   2. Verfahrensfrist
   3. Grenzzeichen
   4. Befristung
   5. Termin
   6. prozessuale Frist
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

233. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'catena alimentare'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'catena alimentare' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lebensmittelkette
   2. Nahrungskette
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

234. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'trasporto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'trasporto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Beförderung
   2. Frachtvertrag
   3. Beförderungsgeschäft
   4. Beförderungsvertrag
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

235. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sgabello a gradini'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sgabello a gradini' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Treppentritt
   2. Rolltritt
   3. tonnenförmiger Tritt
   4. Elefantenfuß
   5. Tritthocker
   6. Tritt
   7. Trittleiter
   8. Rollhocker
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

236. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto vincolato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto vincolato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. gebundener Verwaltungsakt
   2. rechtlich gebundener Akt
   3. rechtlich gebundener Verwaltungsakt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

237. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autonomia statutaria'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autonomia statutaria' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Satzungsautonomie
   2. Satzungsgewalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

238. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'regolamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'regolamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geschäftsordnung
   2. Rechtsverordnung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

239. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'disponibilità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'disponibilità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verfügbarkeit
   2. Kreditrahmen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

240. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ambiente chiuso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ambiente chiuso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. teilweise geschlossener Raum
   2. geschlossener Raum
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

241. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ergonomia organizzativa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ergonomia organizzativa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. kognitive Ergonomie
   2. Organisationsergonomie
   3. körperbezogene Ergonomie
   4. organisatorische Ergonomie
   5. physikalische Ergonomie
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

242. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tutela dei minori'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tutela dei minori' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vormundschaft
   2. Schutz von Minderjährigen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

243. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'aggiornamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'aggiornamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktualisierung
   2. Weiterbildung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

244. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'associato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'associato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. still Beteiligter
   2. Stiller
   3. stiller Gesellschafter
   4. Vereinsmitglied
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

245. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'comunicazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'comunicazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mitteilung
   2. Kommunikation
   3. Bekanntgabe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

246. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'illecito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'illecito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. rechtswidrig
   2. widerrechtlich
   3. Unrecht
   4. unerlaubt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

247. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sezione penale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sezione penale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Strafkammer
   2. Strafsenat
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

248. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'S'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'S' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. geh.
   2. geheim
   3. Leistungsdichte
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

249. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'attività pericolosa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'attività pericolosa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. gefährliche Tätigkeit
   2. gefährliche Unternehmung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

250. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'bene'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'bene' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gut
   2. Sache
   3. Leasing-Objekt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

251. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lista elettorale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lista elettorale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wahlvorschlagliste
   2. Verzeichnis der Wahlberechtigten
   3. Wählerverzeichnis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

252. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'bene'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'bene' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gut
   2. Leasingobjekt
   3. Sache
   4. Leasing-Objekt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

253. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'giustizia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'giustizia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gerechtigkeit
   2. Rechtspflege
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

254. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'parco archeologico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'parco archeologico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Endarchiv
   2. archäologischer Park
   3. Museum
   4. Archiv
   5. Ensemble
   6. Bibliothek
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

255. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'isolamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'isolamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Isolation
   2. Isolierung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

256. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dirigente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dirigente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. leitender Angestellter
   2. Führungskraft
   3. leitender Beamter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

257. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'principio di pubblicità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'principio di pubblicità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Öffentlichkeitsgrundsatz
   2. Öffentlichkeitsprinzip
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

258. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'indumenti di protezione per saldatura'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'indumenti di protezione per saldatura' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Chemikalienschutzkleidung
   2. Hitzeschutzkleidung
   3. UV-Schutzkleidung
   4. Schutzkleidung gegen mechanische Einwirkung
   5. Warnkleidung
   6. Schutzkleidung
   7. Schweißerschutzkleidung
   8. CS-Kleidung
   9. Schutzkleidung gegen mechanische Einwirkungen
   10. Schweißerschutzbekleidung
   11. Wetterschutzkleidung
   12. Kälteschutzkleidung
   13. Staubschutzkleidung
   14. Strahlenschutzkleidung
   15. Gasschutzkleidung
   16. antistatische Schutzkleidung
   17. UV-Schutzbekleidung
   18. antistatische Kleidung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

259. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'scala in appoggio scorrevole'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'scala in appoggio scorrevole' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Anlegeleiter
   2. Rollleiter
   3. verfahrbare Regalleiter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

260. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'incorporazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'incorporazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aufnahme
   2. Verbindung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

261. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto esecutivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto esecutivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vollstreckungshandlung
   2. Ausführungshandlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

262. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'uso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'uso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gebrauchsrecht
   2. Brauch
   3. Gewohnheitsrecht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

263. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'indennizzo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'indennizzo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Enteignungsentschädigung
   2. Entschädigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

264. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verschollener
   2. abwesend
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

265. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'calpestabile'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'calpestabile' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. durchsturzsicher
   2. betretbar
   3. nicht durchsturzsicher
   4. bedingt begehbar
   5. begehbar
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

266. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'efficacia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'efficacia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Effektivität
   2. Wirksamkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

267. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'violenza fisica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'violenza fisica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. physische Gewalt
   2. unmittelbare Gewalt
   3. unmittelbarer körperlicher Zwang
   4. vis absoluta
   5. absolute Gewalt
   6. unwiderstehliche Gerwalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

268. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'custodia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'custodia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Obhut
   2. Aufbewahrung
   3. Verwahrung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

269. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'giudizio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'giudizio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verfahren
   2. Hauptverfahren
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

270. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'destinatario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'destinatario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Nutzer
   2. Empfänger
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

271. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'violenza fisica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'violenza fisica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. unmittelbarer körperlicher Zwang
   2. physische Gewalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

272. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'evento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'evento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ereignis
   2. Erfolg
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

273. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'matrimonio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'matrimonio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Eheschließung
   2. Ehe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

274. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'slitta'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'slitta' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gespannfuhrwerk
   2. Fuhrwerk
   3. Schlitten
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

275. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'matrimonio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'matrimonio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Eheschließung
   2. Heirat
   3. Trauung
   4. Ehe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

276. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'contraente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'contraente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versicherungsnehmer
   2. Partei
   3. Teilnehmer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

277. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'decadenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'decadenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verfall
   2. Verwirkung
   3. Rücknahme
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

278. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione degli occhi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione degli occhi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Augenschutz
   2. Schutz der Augen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

279. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pensione di inabilità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pensione di inabilità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rente wegen voller Erwerbsminderung
   2. volle Erwerbsminderungsrente
   3. Rente wegen teilweiser Erwerbsminderung
   4. teilweise Erwerbsminderungsrente
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

280. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'esame di idoneità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'esame di idoneità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. theoretische Prüfung
   2. Fahrprüfung
   3. praktische Prüfung
   4. Theorieprüfung
   5. Fahrerlaubnisprüfung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

281. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lavoratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lavoratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeitnehmer
   2. erwerbstätige Person
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

282. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'principio di pubblicità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'principio di pubblicità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Öffentlichkeitsprinzip
   2. Prinzip der Öffentlichkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

283. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'mediatore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'mediatore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mäkler
   2. Mediator
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

284. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'replica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'replica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erwiderung
   2. Gegeneinwendung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

285. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autorizzazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autorizzazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erlaubnis
   2. Ermächtigung
   3. Fahrschulerlaubnis
   4. Genehmigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

286. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'archivio corrente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'archivio corrente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwaltungsarchiv
   2. Altablage
   3. Altregistratur
   4. laufendes Archiv
   5. Archiv
   6. Endarchiv
   7. Zwischenarchiv
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

287. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'consuetudine'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'consuetudine' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gewohnheitsrecht
   2. Gewohnheit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

288. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'condizioni di lavoro'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'condizioni di lavoro' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeitsumstände
   2. Arbeitsbedingungen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

289. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'utente finale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'utente finale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Endnutzer
   2. Benutzer
   3. Nutzer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

290. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'indumenti di protezione per saldatura'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'indumenti di protezione per saldatura' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. antistatische Kleidung
   2. UV-Schutzkleidung
   3. Schutzkleidung
   4. Wetterschutzkleidung
   5. Schutzkleidung gegen mechanische Einwirkung
   6. UV-Schutzbekleidung
   7. Kälteschutzkleidung
   8. Warnkleidung
   9. Schweißerschutzkleidung
   10. Gasschutzkleidung
   11. CS-Kleidung
   12. Schweißerschutzbekleidung
   13. Staubschutzkleidung
   14. antistatische Schutzkleidung
   15. Chemikalienschutzkleidung
   16. Hitzeschutzkleidung
   17. Strahlenschutzkleidung
   18. Schutzkleidung gegen mechanische Einwirkungen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

291. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'notifica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'notifica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zustellung
   2. Benennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

292. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'archivio pubblico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'archivio pubblico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Archiv
   2. privates Archiv
   3. Endarchiv
   4. Privatarchiv
   5. öffentliches Archiv
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

293. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'legge'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'legge' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gesetz
   2. G
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

294. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tempo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tempo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zeitraum
   2. Dauer
   3. Zeit
   4. Zeitpunkt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

295. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'addetto antincendio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'addetto antincendio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ersthelfer
   2. Brandschutzhelfer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

296. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pericolo di intossicazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pericolo di intossicazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Intoxikationsgefahr
   2. Gefahr
   3. Vergiftungsgefahr
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

297. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'parte attiva'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'parte attiva' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. aktives Teil
   2. ungeschütztes aktives Teil
   3. unter Spannung stehendes aktives Teil
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

298. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'misura di protezione antincendio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'misura di protezione antincendio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Brandabschnittstrennung
   2. Brandschutzmaßnahme
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

299. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'causa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'causa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtsstreit
   2. Streitsache
   3. Ursache
   4. Rechtsgrund
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

300. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'azione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'azione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Klage
   2. Tun
   3. Handlung
   4. Aktie
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

301. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'utente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'utente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Benutzer
   2. Nutzer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

302. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fondatore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fondatore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Stifter
   2. Gründer
   3. Gründungsaktionär
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

303. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tutela'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tutela' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vormundschaft
   2. Schutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

304. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'bene'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'bene' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sache
   2. Gut
   3. Leasingobjekt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

305. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'condominio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'condominio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wohnungseigentum
   2. Gemeinschaft der Wohnungseigentümer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

306. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'riabilitazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'riabilitazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Suchtrehabilitation
   2. Rehabilitation
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

307. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'violenza fisica'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'violenza fisica' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. physische Gewalt
   2. unmittelbare Gewalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

308. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'patologia da calore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'patologia da calore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hitzeerschöpfung
   2. Hitzeerkrankung
   3. Hitzschlag
   4. Hitzeschlag
   5. Hitzekollaps
   6. Hitzekrampf
   7. Sonnenstich
   8. Hitzekrankheit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

309. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rischio meccanico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rischio meccanico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. thermische Gefährdung
   2. Blaulichtgefährdung
   3. thermisches Risiko
   4. elektrische Gefährdung
   5. Vibrationsgefährdung
   6. mechanische Gefährdung
   7. Lärmgefährdung
   8. Vibrationsrisiko
   9. Blue Light Hazard
   10. Lärmrisiko
   11. physikalisches Risiko
   12. physikalische Gefährdung
   13. elektrisches Risiko
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

310. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assemblea dei condomini'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assemblea dei condomini' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wohnungseigentümerversammlung
   2. Versammlung der Wohnungseigentümer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

311. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'generalità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'generalità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Allgemeinheit
   2. Personalien
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

312. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'circuito PELV'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'circuito PELV' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. ELV-Stromkreis
   2. SELV-Stromkreis
   3. PELV-Stromkreis
   4. FELV-Stromkreis
   5. Kleinspannungsstromkreis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

313. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'vaccino multivalente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'vaccino multivalente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mehrfachimpfstoff
   2. Impfstoff
   3. monovalenter Impfstoff
   4. Einfachimpfstoff
   5. Kombinationsimpfstoff
   6. Einzelimpfstoff
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

314. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'prevenzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'prevenzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vorbeugung
   2. Prävention
   3. Verhütung
   4. vorbeugende Konservierung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

315. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'IR'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'IR' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. ionisierende Strahlung
   2. Infrarot-Strahlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

316. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'periodo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'periodo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Satz
   2. Zeitraum
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

317. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'doloso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'doloso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. arglistig
   2. vorsätzlich
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

318. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'accesso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'accesso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zufahrt
   2. Zugangsöffnung
   3. Zutritt
   4. Zugang
   5. Zugangsrecht
   6. Zutrittsrecht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

319. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'legittimità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'legittimità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtmäßigkeit
   2. eheliche Abstammung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

320. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'efficienza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'efficienza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Effektivität
   2. Effizienz
   3. Wirksamkeit
   4. Rechtswirksamkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

321. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'legalizzazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'legalizzazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Beglaubigung der Unterschrift
   2. Legalisation
   3. Zertifizierung
   4. Unterschriftsbeglaubigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

322. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'emissione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'emissione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ausgabe
   2. Emission
   3. Begebung
   4. Emissionen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

323. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assemblea'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assemblea' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mitgliederversammlung
   2. Hauptversammlung
   3. Versammlumg der Mitglieder
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

324. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'corrente di contatto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'corrente di contatto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. elektrischer Strom
   2. stationärer Kontaktstrom
   3. Kontaktstrom
   4. Strom
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

325. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'associazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'associazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verein
   2. Vereinigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

326. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lavaocchi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lavaocchi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Augennotdusche
   2. Augendusche
   3. Augenspüleinrichtung
   4. Augenspülflasche
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

327. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tampone nasofaringeo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tampone nasofaringeo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. oropharyngealer Abstrich
   2. Nasopharynx-Abstrich
   3. Oropharyngealabstrich
   4. PCR-Test
   5. Oropharynx-Abstrich
   6. Nasopharyngealabstrich
   7. nasopharyngealer Abstrich
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

328. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'segnale di precedenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'segnale di precedenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gebotszeichen
   2. Vorschriftszeichen
   3. Vorfahrtszeichen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

329. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'amministratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'amministratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verwalter
   2. Geschäftsführer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

330. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'termine'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'termine' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Grenzzeichen
   2. Verfahrensfrist
   3. Frist
   4. Termin
   5. Befristung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

331. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lavoratore autonomo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lavoratore autonomo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Freiberufler
   2. Freelancer
   3. Selbstständiger
   4. Handwerker
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

332. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'associato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'associato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mitglied
   2. Vereinsmitglied
   3. stiller Gesellschafter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

333. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'agrotecnico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'agrotecnico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Agrarbetriebswirt
   2. Agrarwissenschaftler
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

334. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'strada principale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'strada principale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hauptverkehrsstraße
   2. Autobahn
   3. Straße
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

335. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'regolamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'regolamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verordnung
   2. Rechtsverordnung
   3. Geschäftsordnung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

336. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ordine pubblico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ordine pubblico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. öffentliche Ordnung
   2. ordre public
   3. öffentliche Sicherheit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

337. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fuoco di metalli'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fuoco di metalli' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Metallbrand
   2. Brand
   3. Brandstiftung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

338. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'potere esecutivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'potere esecutivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. vollziehende Gewalt
   2. Exekutive
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

339. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'quota'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'quota' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Geschäftsanteil
   2. Anteil
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

340. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'potere legislativo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'potere legislativo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Legislative
   2. gesetzgebende Gewalt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

341. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'lavoratore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'lavoratore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeitnehmer
   2. Erwerbstätiger
   3. erwerbstätige Person
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

342. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'mandante'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'mandante' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Auftraggeber
   2. Versender
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

343. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'minaccia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'minaccia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Drohung
   2. Androhung
   3. Bedrohung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

344. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fiduciario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fiduciario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Treuhänder
   2. Betreuer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

345. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione degli occhi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione degli occhi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutz der Augen
   2. Augenschutzgerät
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

346. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'riconoscimento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'riconoscimento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wiedererkennen
   2. Anerkennung
   3. Identifizierung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

347. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'mediatore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'mediatore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Makler
   2. Mediator
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

348. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'condominio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'condominio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gemeinschaft der Wohnungseigentümer
   2. Wohnungseigentum
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

349. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tipo di esposizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tipo di esposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Expositionsart
   2. Exposition
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

350. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'illecito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'illecito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. unerlaubte Handlung
   2. rechtswidriges Verhalten
   3. Unrecht
   4. widerrechtlich
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

351. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'principio del libero convincimento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'principio del libero convincimento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Grundsatz der freien richterlichen Beweiswürdigung
   2. Grundsatz der freien Beweiswürdigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

352. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'obbligo di informazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'obbligo di informazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Informationspflicht
   2. Erkundigungspflicht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

353. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto processuale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto processuale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aktenstück
   2. Verfahrenshandlung
   3. Aktenteil
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

354. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'recidivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'recidivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rückfalltäter
   2. rückfällig
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

355. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'organizzazione del lavoro'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'organizzazione del lavoro' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeitsablauf
   2. Arbeitsorganisation
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

356. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'locatario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'locatario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Mieter
   2. Leasingnehmer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

357. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione delle gambe'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione delle gambe' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutz der Beine
   2. Beinschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

358. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sicurezza sul lavoro'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sicurezza sul lavoro' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Arbeitssicherheit
   2. Arbeitsschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

359. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispositivo di protezione individuale contro le cadute dall'alto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. PSA gegen Absturz
   2. persönliche Schutzausrüstung
   3. PSAgA
   4. Arbeitsplatzpositionierungssystem
   5. Höhensicherungsgerät
   6. Auffangsystem
   7. Rückhaltesystem
   8. PSA
   9. Schutzausrüstung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

360. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'vaccino multivalente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'vaccino multivalente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. monovalenter Impfstoff
   2. Impfstoff
   3. Einzelimpfstoff
   4. Einfachimpfstoff
   5. Kombinationsimpfstoff
   6. Mehrfachimpfstoff
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

361. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto esecutivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto esecutivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ausführungshandlung
   2. Vollzugsakt
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

362. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'legale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'legale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. rechtsgültig
   2. gesetzesmäßig
   3. gesetzmäßig
   4. gesetzlich
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

363. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'deposito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'deposito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Aufbewahrung
   2. Lagern
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

364. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'istruzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'istruzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vorbereitung der Entscheidung
   2. Ausbildung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

365. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'decadenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'decadenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rücknahme
   2. Verfall
   3. Verwirkung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

366. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dovere di fedeltà'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dovere di fedeltà' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Treuepflicht
   2. Pflicht zur ehelichen Treue
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

367. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'premio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'premio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versicherungsprämie
   2. Prämie
   3. Preis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

368. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispensa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispensa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Befreiung
   2. Dispens
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

369. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'promittente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'promittente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verlobter
   2. Versprechender
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

370. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'conservazione dei beni culturali'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'conservazione dei beni culturali' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Konservierung
   2. Denkmalpflege
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

371. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'emissione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'emissione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schadstoffemissionen
   2. Emissionen
   3. Ausgabe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

372. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'cauzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'cauzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sicherheitsleistung
   2. Kaution
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

373. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'legale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'legale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. rechtsgültig
   2. gesetzmäßig
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

374. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'termine'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'termine' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. prozessuale Frist
   2. Befristung
   3. Grenzzeichen
   4. Verfahrensfrist
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

375. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'onere'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'onere' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Auflage
   2. Obliegenheit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

376. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'archivio corrente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'archivio corrente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. laufende Registratur
   2. laufende Ablage
   3. laufendes Archiv
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

377. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'causa'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'causa' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rechtsgrund
   2. Ursache
   3. causa
   4. Rechtsstreit
   5. Streitsache
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

378. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'principio di pubblicità'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'principio di pubblicità' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Öffentlichkeitsprinzip
   2. Grundsatz der Wirtschaftlichkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

379. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'grembiule antitaglio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'grembiule antitaglio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schnittschutzkleidung
   2. Schutzschürze
   3. Schnittschutzschürze
   4. Schnittschutzhose
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

380. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'concedente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'concedente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hersteller
   2. Leasinggeber
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

381. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'prevenzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'prevenzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. präventive Konservierung
   2. Vorbeugung
   3. Verhütung
   4. Prävention
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

382. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'contraddittorio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'contraddittorio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Anhörung
   2. rechtliches Gehör
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

383. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'società incorporante'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'società incorporante' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. neuer Rechtsträger
   2. übernehmende Gesellschaft
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

384. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'radiazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'radiazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Abmeldung
   2. Strahlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

385. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'esecuzione forzata di obblighi di fare'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'esecuzione forzata di obblighi di fare' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zwangsvollstreckung zur Erwirkung vertretbarer Handlungen
   2. Zwangsvollstreckung zur Erwirkung nicht vertretbarer Handlungen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

386. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione delle gambe'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione delle gambe' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Beinschutz
   2. Schutz der Beine
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

387. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'riserva'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'riserva' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Pflichtteil
   2. Vorbehalt
   3. Rücklage
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

388. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'aggiornamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'aggiornamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Berufsfortbildung
   2. Aktualisierung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

389. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'separazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'separazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Getrenntleben
   2. Trennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

390. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'inquinamento acustico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'inquinamento acustico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Verunreinigung
   2. Lärmbelastung
   3. Verschmutzung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

391. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'comunicazione diretta'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'comunicazione diretta' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Ruf- und Sichtverbindung
   2. Verbindung über andere Mittel
   3. ständige Verbindung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

392. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'recidivo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'recidivo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. rückfällig
   2. Rückfalltäter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

393. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'atto materiale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'atto materiale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. nichtförmliches Verwaltungshandeln
   2. Realakt
   3. Tathandlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

394. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'livello di azione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'livello di azione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Auslösewert
   2. Interventionsschwelle
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

395. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'VIS'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'VIS' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gesundheitsverträglichkeitsprüfung
   2. sichtbare Strahlung
   3. GVP
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

396. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'diritto di voto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'diritto di voto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wahlrecht
   2. Stimmrecht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

397. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'intensità dell'esposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Exposition
   2. Einwirkdauer
   3. Einwirkungsdauer
   4. Expositionsausmaß
   5. Expositionsdauer
   6. Expositionsart
   7. Expositionsintensität
   8. Expositionswert
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

398. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'produttore'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'produttore' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Hersteller
   2. Abfallerzeuger
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

399. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'circolazione pedonale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'circolazione pedonale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Fußgängerverkehr
   2. Kraftfahrzeugverkehr
   3. Verkehr
   4. Fahrzeugverkehr
   5. Straßenverkehr
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

400. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'arco elettrico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'arco elettrico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Störlichtbogen
   2. Lichtbogen
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

401. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'esposizione alle radiazioni'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'esposizione alle radiazioni' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Vibrationsexposition
   2. Strahlungsexposition
   3. Asbestexposition
   4. UV-Exposition
   5. Lärmexposition
   6. Exposition
   7. UV-Strahlungsexposition
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

402. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ricorso in opposizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ricorso in opposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Widerspruch
   2. Aufsichtsbeschwerde
   3. Einspruch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

403. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'assente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'assente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. abwesend
   2. Verschollener
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

404. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'a constrained term'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione dell'udito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Gehörschutz
   2. Schutz des Gehörs
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

405. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'diritto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'diritto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. subjektives Recht
   2. objektives Recht
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

406. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'infortunio sul lavoro'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'infortunio sul lavoro' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wegeunfall
   2. Unfall
   3. Arbeitsunfall
   4. Dienstwegeunfall
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

407. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'bene'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'bene' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Leasingobjekt
   2. Sache
   3. Leasing-Objekt
   4. Gut
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

408. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'concessionario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'concessionario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Konzessionär
   2. Vertragshändler
   3. Eigenhändler
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

409. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'cosa comune'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'cosa comune' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. gemeinschaftlicher Gegenstand
   2. Gemeingut
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

410. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'pulsante di arresto di emergenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'pulsante di arresto di emergenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Not-Halt-Befehlsgerät
   2. Not-Halt-Taster
   3. Not-Halt-Gerät
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

411. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'certificato di residenza'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'certificato di residenza' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Bescheinigung
   2. Meldebescheinigung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

412. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'arresto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'arresto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Freiheitsstrafe
   2. Festnahme
   3. Warten
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

413. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'libretto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'libretto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zulassungsbescheinigung
   2. Sparbuch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

414. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'straniero'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'straniero' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. ausländisch
   2. Ausländer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

415. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione delle mani'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione delle mani' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Handschutz
   2. Schutz der Hände
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

416. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'commissione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'commissione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kommissionsvertrag
   2. Kommission
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

417. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'essentialia negotii'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'essentialia negotii' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. wesentliche Vertragsbestandteile
   2. notwendige Bestandteile
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

418. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'domanda'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'domanda' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Anspruch
   2. Gesuch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

419. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'locatario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'locatario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Leasingnehmer
   2. Mieter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

420. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'annullamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'annullamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kraftloserklärung von Aktien
   2. Anfechtung
   3. Rücknahme mit Rückwirkung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

421. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fiamme libere'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fiamme libere' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Zündquelle
   2. offenes Feuer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

422. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'candidato'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'candidato' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kandidat
   2. Bewerber
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

423. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rischio di scivolamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rischio di scivolamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Sturz- und Absturzrisiko
   2. Stolpergefährdung
   3. Gefährdung
   4. Risiko
   5. Gefahr
   6. Sturz- und Absturzgefährdung
   7. Rutschgefährdung
   8. Rutschrisiko
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

424. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'premio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'premio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Versicherungsprämie
   2. Preis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

425. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'VIS'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'VIS' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. sichtbares Licht
   2. GVP
   3. Gesundheitsverträglichkeitsprüfung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

426. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'affidamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'affidamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Pflegekindschaft
   2. Vergabe
   3. Fremdunterbringung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

427. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'collusione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'collusione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. rechtswidrige Absprache
   2. Kollusion
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

428. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dispositivo di protezione dei piedi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dispositivo di protezione dei piedi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Fußschutz
   2. persönliche Schutzausrüstung
   3. Schutzschuh
   4. Schutzausrüstung
   5. Fußschutzausrüstung
   6. Sicherheitsschuh
   7. Berufsschuh
   8. PSA
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

429. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autorizzazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autorizzazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Erlaubnis
   2. Fahrschulerlaubnis
   3. Genehmigung
   4. behördliche Erlaubnis
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

430. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'prevenzione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'prevenzione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. passive Konservierung
   2. Vorbeugung
   3. Verhütung
   4. Prävention
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

431. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'classe di isolamento elettrico'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'classe di isolamento elettrico' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutzklasse II
   2. Schutzklasse
   3. Schutzklasse III
   4. Schutzklasse I
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

432. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'RR'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'RR' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. VS-Vertr.
   2. Wiederholungsrezept
   3. Verschreibung zur wiederholten Abgabe
   4. Wiederholungsverordnung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

433. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'autonomia funzionale'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'autonomia funzionale' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. funktionale Selbstverwaltung
   2. funktionale Selbstverwaltungskörperschaft
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

434. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'forma vincolata'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'forma vincolata' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Formzwang
   2. gesetzlich vorgeschriebene Form
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

435. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'agente biologico del gruppo 3'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'agente biologico del gruppo 3' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. biologischer Arbeitsstoff
   2. Biostoff
   3. Biostoff der Risikogruppe 2
   4. Biostoff der Risikogruppe 4
   5. Biostoff der Risikogruppe 3
   6. Biostoff der Risikogruppe 1
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

436. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'codice di identificazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'codice di identificazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Identifizierungsnummer
   2. Kennnummer
   3. Kennziffer
   4. Identifikationsnummer
   5. Kennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

437. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'codice di identificazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'codice di identificazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Benutzerkennung
   2. Identifizierungsnummer
   3. Kennung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

438. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'tutela dei beni culturali'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'tutela dei beni culturali' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Denkmalschutz
   2. Denkmalpflege
   3. Kulturgutschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

439. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'ricorrente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'ricorrente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Revisionsbeklagter
   2. Beschwerdeführer
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

440. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Schutzeinrichtung
   2. Schutz
   3. Schutzvorrichtung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

441. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'zona di preselezione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'zona di preselezione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Fahrbahn
   2. Vorsortierraum
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

442. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'rischio di esposizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'rischio di esposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Expositionsrisiko
   2. Expositionsgefährdung
   3. Expositionsrisiko gegenüber Asbestfasern
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

443. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'recupero'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'recupero' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rehabilitation
   2. Abfallverwertung
   3. Suchtrehabilitation
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

444. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'titolo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'titolo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Titel
   2. Überschrift
   3. Rechtsgrund
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

445. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'arresto'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'arresto' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Warten
   2. Verhaftung
   3. Festnahme
   4. Freiheitsstrafe
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

446. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'agente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'agente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Täter
   2. Arbeitsstoff
   3. Handelsvertreter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

447. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'fondo'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'fondo' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Grundstück
   2. Fonds
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

448. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'buona fede'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'buona fede' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. guter Glaube
   2. Treu und Glauben
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

449. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'barriera antincendio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'barriera antincendio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Brandabschnittstrennung
   2. Brandschutzmaßnahme
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

450. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'VIS'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'VIS' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. GVP
   2. Gesundheitsverträglichkeitsprüfung
   3. VIS
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

451. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'disposizione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'disposizione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Bestimmung
   2. Verfügung
   3. Anordnung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

452. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'zona sorvegliata'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'zona sorvegliata' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Überwachungsbereich
   2. Kontrollbereich
   3. Strahlenschutzbereich
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

453. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'deposito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'deposito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lagern
   2. Verwahrung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

454. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'dirigente'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'dirigente' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Leiter
   2. Führungskraft
   3. leitender Angestellter
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

455. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'sistema PELV'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'sistema PELV' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. SELV-System
   2. FELV-System
   3. PELV-System
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

456. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'annullamento'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'annullamento' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Rücknahme mit Rückwirkung
   2. Anfechtung
   3. Kraftloserklärung von Aktien
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

457. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'deposito'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'deposito' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Lagern
   2. Verwahrungsvertrag
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

458. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'svalutazione'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'svalutazione' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Abwertung
   2. Geldentwertung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

459. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'patente di servizio'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'patente di servizio' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Führerschein
   2. Dienstführerschein
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

460. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'IR'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'IR' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Infrarotstrahlung
   2. ionisierende Strahlung
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

461. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'efficacia'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'efficacia' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Wirksamkeit
   2. Effektivität
   3. Rechtswirksamkeit
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

462. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'protezione degli occhi'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'protezione degli occhi' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Augenschutzgerät
   2. Schutz der Augen
   3. Augenschutz
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

463. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'uso'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'uso' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Benutzungsrecht
   2. Gewohnheitsrecht
   3. Gebrauchsrecht
   4. Brauch
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

464. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'marciapiede'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'marciapiede' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Straße
   2. Gehweg
   3. Bürgersteig
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

465. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'forma vincolata'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'forma vincolata' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. gesetzlich vorgeschriebene Form
   2. Formzwang
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

466. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'catasto fondiario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'catasto fondiario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Kataster
   2. Liegenschaftskataster
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

467. `1` rows | `legal_it_to_de_with_term_constraints`
   German legal (Italy->Germany) with term-choice constraint for 'intermediario'.

   Raw instruction:

   ```text
   You are a professional legal translator specializing in Italian-to-German translation for the legal system of Germany.
   Your task is to translate a legal sentence from Italian into the standard variety of German used in Germany without dialectal expressions, ensuring that the translation is fully aligned with the legal terminology, conventions, and drafting style of that jurisdiction. The translation must preserve the exact legal meaning and reflect how such concepts are expressed within the legal system of Germany, so that the result can function as an authoritative legal text.
   There are terminological constraints you must adhere to:
   'The Italian term 'intermediario' must be translated using exactly one candidate from the list below:
   <CANDIDATES>
   1. Makler von Abfällen
   2. Mittelsmann
   </CANDIDATES>
   To select the correct equivalent, choose the term that best matches its meaning within the legal context of Germany. Do not reproduce the candidate label in the output. You must output only the translated text without any explanation.
   This is the text to be translated into German German (de_DE):
   ```

### `deu_Latn`
- Rows: `513`
- Unique instructions: `5`
- Instruction clusters: `professional_translator_czech_education_html` x 1, `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `247` rows | `professional_translator_spoken_asr`
   German: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional German translator, tasked with providing translations suitable for use in German (deu_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to German grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the German translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into German (deu_Latn):
   ```

2. `117` rows | `professional_translator_social_media`
   German: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional German translator, tasked with providing translations suitable for use in German (deu_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to German grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in German. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the German translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into German (deu_Latn):
   ```

3. `79` rows | `professional_translator_news_html`
   German: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional German translator, tasked with providing translations suitable for use in German (deu_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to German grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the German translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into German (deu_Latn):
   ```

4. `63` rows | `professional_translator_czech_education_html`
   German: Czech educational exercises prompt; preserve HTML.

   Raw instruction:

   ```text
   You are a professional German translator, tasked with providing translations suitable for use in German (deu_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to German grammar and vocabulary and ensuring that the translation is natural. The original Czech text consists of biology, chemistry, and geography exercises extracted from an educational web portal for children aged 9-16. Produce only the German translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into German (deu_Latn):
   ```

5. `7` rows | `professional_translator_software_json`
   German: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional German translator, tasked with providing translations suitable for use in German (deu_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to German grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the German translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into German (deu_Latn):
   ```

### `ekk_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Estonian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Estonian translator, tasked with providing translations suitable for use in Estonian (ekk_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Estonian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Estonian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Estonian (ekk_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Estonian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Estonian translator, tasked with providing translations suitable for use in Estonian (ekk_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Estonian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Estonian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Estonian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Estonian (ekk_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Estonian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Estonian translator, tasked with providing translations suitable for use in Estonian (ekk_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Estonian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Estonian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Estonian (ekk_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Estonian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Estonian translator, tasked with providing translations suitable for use in Estonian (ekk_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Estonian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Estonian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Estonian (ekk_Latn):
   ```

### `et_EE`
- Rows: `917`
- Unique instructions: `1`
- Instruction clusters: `simple_code_direction` x 1

1. `917` rows | `simple_code_direction`
   Translate from en to et_EE.

   Raw instruction:

   ```text
   Translate from en to et_EE.
   ```

### `hye_Armn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Eastern Armenian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Eastern Armenian translator, tasked with providing translations suitable for use in Eastern Armenian (hye_Armn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Eastern Armenian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Eastern Armenian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Eastern Armenian (hye_Armn):
   ```

2. `44` rows | `professional_translator_social_media`
   Eastern Armenian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Eastern Armenian translator, tasked with providing translations suitable for use in Eastern Armenian (hye_Armn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Eastern Armenian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Eastern Armenian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Eastern Armenian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Eastern Armenian (hye_Armn):
   ```

3. `14` rows | `professional_translator_news_html`
   Eastern Armenian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Eastern Armenian translator, tasked with providing translations suitable for use in Eastern Armenian (hye_Armn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Eastern Armenian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Eastern Armenian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Eastern Armenian (hye_Armn):
   ```

4. `7` rows | `professional_translator_software_json`
   Eastern Armenian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Eastern Armenian translator, tasked with providing translations suitable for use in Eastern Armenian (hye_Armn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Eastern Armenian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Eastern Armenian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Eastern Armenian (hye_Armn):
   ```

### `ind_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Indonesian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Indonesian translator, tasked with providing translations suitable for use in Indonesian (ind_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Indonesian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Indonesian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Indonesian (ind_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Indonesian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Indonesian translator, tasked with providing translations suitable for use in Indonesian (ind_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Indonesian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Indonesian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Indonesian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Indonesian (ind_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Indonesian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Indonesian translator, tasked with providing translations suitable for use in Indonesian (ind_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Indonesian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Indonesian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Indonesian (ind_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Indonesian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Indonesian translator, tasked with providing translations suitable for use in Indonesian (ind_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Indonesian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Indonesian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Indonesian (ind_Latn):
   ```

### `is`
- Rows: `345`
- Unique instructions: `1`
- Instruction clusters: `simple_named_direction` x 1

1. `345` rows | `simple_named_direction`
   Translate from English to Icelandic.

   Raw instruction:

   ```text
   Translate from English to Icelandic.
   ```

### `isl_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Icelandic: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Icelandic translator, tasked with providing translations suitable for use in Icelandic (isl_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Icelandic grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Icelandic translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Icelandic (isl_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Icelandic: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Icelandic translator, tasked with providing translations suitable for use in Icelandic (isl_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Icelandic grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Icelandic. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Icelandic translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Icelandic (isl_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Icelandic: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Icelandic translator, tasked with providing translations suitable for use in Icelandic (isl_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Icelandic grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Icelandic translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Icelandic (isl_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Icelandic: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Icelandic translator, tasked with providing translations suitable for use in Icelandic (isl_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Icelandic grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Icelandic translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Icelandic (isl_Latn):
   ```

### `jpn_Jpan`
- Rows: `388`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `247` rows | `professional_translator_spoken_asr`
   Japanese: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Japanese translator, tasked with providing translations suitable for use in Japanese (jpn_Jpan). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Japanese grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Japanese translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Japanese (jpn_Jpan):
   ```

2. `92` rows | `professional_translator_social_media`
   Japanese: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Japanese translator, tasked with providing translations suitable for use in Japanese (jpn_Jpan). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Japanese grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Japanese. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Japanese translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Japanese (jpn_Jpan):
   ```

3. `42` rows | `professional_translator_news_html`
   Japanese: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Japanese translator, tasked with providing translations suitable for use in Japanese (jpn_Jpan). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Japanese grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Japanese translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Japanese (jpn_Jpan):
   ```

4. `7` rows | `professional_translator_software_json`
   Japanese: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Japanese translator, tasked with providing translations suitable for use in Japanese (jpn_Jpan). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Japanese grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Japanese translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Japanese (jpn_Jpan):
   ```

### `kaz_Cyrl`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Kazakh: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Kazakh translator, tasked with providing translations suitable for use in Kazakh (kaz_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Kazakh grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Kazakh translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Kazakh (kaz_Cyrl):
   ```

2. `44` rows | `professional_translator_social_media`
   Kazakh: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Kazakh translator, tasked with providing translations suitable for use in Kazakh (kaz_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Kazakh grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Kazakh. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Kazakh translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Kazakh (kaz_Cyrl):
   ```

3. `14` rows | `professional_translator_news_html`
   Kazakh: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Kazakh translator, tasked with providing translations suitable for use in Kazakh (kaz_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Kazakh grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Kazakh translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Kazakh (kaz_Cyrl):
   ```

4. `7` rows | `professional_translator_software_json`
   Kazakh: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Kazakh translator, tasked with providing translations suitable for use in Kazakh (kaz_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Kazakh grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Kazakh translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Kazakh (kaz_Cyrl):
   ```

### `ko_KR`
- Rows: `1880`
- Unique instructions: `51`
- Instruction clusters: `simple_code_direction` x 1, `wesnoth_dialogue_persona_conditioned` x 50

1. `1644` rows | `simple_code_direction`
   Translate from en to ko_KR.

   Raw instruction:

   ```text
   Translate from en to ko_KR.
   ```

2. `31` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Prince Haldric, a member of royalty or high nobility; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Prince Haldric, a member of royalty or high nobility. Their in-game unit type is Noble Commander. In this line the speaker is speaking (exclam). As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

3. `17` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lady Dionli, a magical being (mage, elf-lord, fae, or undead lich); speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lady Dionli, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Autumn Shyde. In this line the speaker is making a statement. As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

4. `16` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Konrad, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Konrad, a military commander, knight, or officer. Their in-game unit type is Commander. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

5. `15` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lady Jessene, a member of royalty or high nobility; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lady Jessene, a member of royalty or high nobility. In this line the speaker is making a statement. As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

6. `15` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Prince Haldric, a member of royalty or high nobility; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Prince Haldric, a member of royalty or high nobility. In this line the speaker is making a statement. As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

7. `11` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Prince Haldric, a member of royalty or high nobility; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Prince Haldric, a member of royalty or high nobility. Their in-game unit type is Noble Commander. In this line the speaker is making a statement. As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

8. `9` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Baldras, a commoner — a peasant, bandit, or outlaw; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Baldras, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Bandit. In this line the speaker is making a statement. As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

9. `9` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Baldras, a commoner — a peasant, bandit, or outlaw; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Baldras, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Highwayman. In this line the speaker is making a statement. As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

10. `8` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Commander Aethyr, a military commander, knight, or officer; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Commander Aethyr, a military commander, knight, or officer. In this line the speaker is making a statement. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

11. `7` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Commander Aethyr, a military commander, knight, or officer; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Commander Aethyr, a military commander, knight, or officer. Their in-game unit type is Lieutenant. In this line the speaker is making a statement. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

12. `7` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Growloff, a commoner — a peasant, bandit, or outlaw; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Growloff, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Ranger. In this line the speaker is speaking (exclam). As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

13. `6` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lady Jessene, a member of royalty or high nobility; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lady Jessene, a member of royalty or high nobility. In this line the speaker is speaking (exclam). As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

14. `6` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=King Addroran IX, a military commander, knight, or officer; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is King Addroran IX, a military commander, knight, or officer. Their in-game unit type is Grand Knight. In this line the speaker is making a statement. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

15. `5` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Growloff, a commoner — a peasant, bandit, or outlaw; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Growloff, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Ranger. In this line the speaker is making a statement. As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

16. `5` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Dommel, a member of royalty or high nobility; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Dommel, a member of royalty or high nobility. Their in-game unit type is General. In this line the speaker is speaking (exclam). As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

17. `4` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Tinry the Red, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Tinry the Red, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Arch Mage. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

18. `4` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Baldras, a commoner — a peasant, bandit, or outlaw; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Baldras, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Highwayman. In this line the speaker is speaking (exclam). As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

19. `3` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Tarwen, a military commander, knight, or officer; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Tarwen, a military commander, knight, or officer. In this line the speaker is making a statement. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

20. `3` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Daellyn the Red, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Daellyn the Red, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Arch Mage. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

21. `3` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lady Outlaw, a member of royalty or high nobility; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lady Outlaw, a member of royalty or high nobility. In this line the speaker is speaking (exclam). As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

22. `3` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Baldras, a commoner — a peasant, bandit, or outlaw; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Baldras, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Bandit. In this line the speaker is speaking (exclam). As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

23. `3` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mel Daveth, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mel Daveth, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Necromancer. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

24. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Glimir, a military commander, knight, or officer; speech_act=speaking (command); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Glimir, a military commander, knight, or officer. Their in-game unit type is Elvish Marshal. In this line the speaker is speaking (command). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

25. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Commander Aethyr, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Commander Aethyr, a military commander, knight, or officer. Their in-game unit type is Lieutenant. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

26. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Tarwen, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Tarwen, a military commander, knight, or officer. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

27. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Glimir, a military commander, knight, or officer; speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Glimir, a military commander, knight, or officer. Their in-game unit type is Elvish Marshal. In this line the speaker is making a statement. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

28. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Galdrad, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Galdrad, a military commander, knight, or officer. Their in-game unit type is Elvish Champion. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

29. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lich-Lord Caror, a magical being (mage, elf-lord, fae, or undead lich); speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lich-Lord Caror, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Lich. In this line the speaker is making a statement. As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

30. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lich-Lord Lenvan, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lich-Lord Lenvan, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Lich. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

31. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Afalas, a commoner — a peasant, bandit, or outlaw; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Afalas, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Outlaw. In this line the speaker is speaking (exclam). As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

32. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mal-Kevek, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mal-Kevek, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Lich. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

33. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Chantal, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Chantal, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Elvish Shyde. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

34. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Southbay Guard 1, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Southbay Guard 1, a military commander, knight, or officer. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

35. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=King Addroran IX, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is King Addroran IX, a military commander, knight, or officer. Their in-game unit type is Grand Knight. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

36. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Growloff, a commoner — a peasant, bandit, or outlaw; speech_act=asking a question; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Growloff, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Ranger. In this line the speaker is asking a question. As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

37. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Baldras, a commoner — a peasant, bandit, or outlaw; speech_act=asking a question; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Baldras, a commoner — a peasant, bandit, or outlaw. Their in-game unit type is Highwayman. In this line the speaker is asking a question. As a commoner, the speaker holds low social standing and speaks plainly, without courtly formality. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

38. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mel Daveth, a magical being (mage, elf-lord, fae, or undead lich); speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mel Daveth, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Necromancer. In this line the speaker is making a statement. As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

39. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mel Guthrak, a magical being (mage, elf-lord, fae, or undead lich); speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mel Guthrak, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Necromancer. In this line the speaker is speaking (exclam). As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

40. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Commander Aethyr, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Commander Aethyr, a military commander, knight, or officer. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

41. `2` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Archarel, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Archarel, a military commander, knight, or officer. Their in-game unit type is Lieutenant. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

42. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mal-Kevek, a magical being (mage, elf-lord, fae, or undead lich); speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mal-Kevek, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Lich. In this line the speaker is making a statement. As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

43. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=King Addroran IX, a military commander, knight, or officer; speech_act=asking a question; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is King Addroran IX, a military commander, knight, or officer. Their in-game unit type is Grand Knight. In this line the speaker is asking a question. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

44. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Kwili, a member of royalty or high nobility; speech_act=speaking (command); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Kwili, a member of royalty or high nobility. In this line the speaker is speaking (command). As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

45. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mal-Yrna, a magical being (mage, elf-lord, fae, or undead lich); speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mal-Yrna, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Necromancer. In this line the speaker is making a statement. As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

46. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lady Jessene, a member of royalty or high nobility; speech_act=asking a question; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lady Jessene, a member of royalty or high nobility. In this line the speaker is asking a question. As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

47. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lord Maddock, a member of royalty or high nobility; speech_act=asking a question; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lord Maddock, a member of royalty or high nobility. In this line the speaker is asking a question. As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

48. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Prince Haldric, a member of royalty or high nobility; speech_act=speaking (command); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Prince Haldric, a member of royalty or high nobility. Their in-game unit type is Noble Commander. In this line the speaker is speaking (command). As royalty, the speaker holds the highest social standing in the scene and normally addresses subjects, advisors, and peers from a position of inherited authority. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

49. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Mal-Govon, a magical being (mage, elf-lord, fae, or undead lich); speech_act=making a statement; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Mal-Govon, a magical being (mage, elf-lord, fae, or undead lich). Their in-game unit type is Lich. In this line the speaker is making a statement. As a magical being, the speaker stands apart from the mortal social order; benevolent fae and elf-lords carry an elevated, archaic bearing, while liches and necromancers speak with arrogant disdain. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

50. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Lord Logalmier, a military commander, knight, or officer; speech_act=asking a question; Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Lord Logalmier, a military commander, knight, or officer. Their in-game unit type is Elvish Champion Kalian. In this line the speaker is asking a question. As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

51. `1` rows | `wesnoth_dialogue_persona_conditioned`
   Wesnoth dialogue: speaker=Alber, a military commander, knight, or officer; speech_act=speaking (exclam); Korean honorific/register control.

   Raw instruction:

   ```text
   Translate the following line of dialogue from the fantasy strategy game Battle for Wesnoth from English (en) to Korean (ko_KR). The speaker is Alber, a military commander, knight, or officer. Their in-game unit type is Lieutenant. In this line the speaker is speaking (exclam). As an officer, the speaker stands in a chain of command: deferential toward superiors and a higher-born, commanding toward subordinates, soldiers, and enemies. Choose Korean speech levels, honorifics, sentence endings, and tone that are consistent with this speaker's social standing and their relationship to the person being addressed. Provide only the Korean translation.
   ```

### `kor_Hang`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Korean: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Korean translator, tasked with providing translations suitable for use in Korean (kor_Hang). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Korean grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Korean translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Korean (kor_Hang):
   ```

2. `44` rows | `professional_translator_social_media`
   Korean: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Korean translator, tasked with providing translations suitable for use in Korean (kor_Hang). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Korean grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Korean. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Korean translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Korean (kor_Hang):
   ```

3. `14` rows | `professional_translator_news_html`
   Korean: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Korean translator, tasked with providing translations suitable for use in Korean (kor_Hang). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Korean grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Korean translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Korean (kor_Hang):
   ```

4. `7` rows | `professional_translator_software_json`
   Korean: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Korean translator, tasked with providing translations suitable for use in Korean (kor_Hang). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Korean grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Korean translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Korean (kor_Hang):
   ```

### `lij_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Ligurian, Italy: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Ligurian, Italy translator, tasked with providing translations suitable for use in Ligurian, Italy (lij_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ligurian, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Ligurian, Italy translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Ligurian, Italy (lij_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Ligurian, Italy: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Ligurian, Italy translator, tasked with providing translations suitable for use in Ligurian, Italy (lij_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ligurian, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Ligurian, Italy. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Ligurian, Italy translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ligurian, Italy (lij_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Ligurian, Italy: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Ligurian, Italy translator, tasked with providing translations suitable for use in Ligurian, Italy (lij_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ligurian, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Ligurian, Italy translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ligurian, Italy (lij_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Ligurian, Italy: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Ligurian, Italy translator, tasked with providing translations suitable for use in Ligurian, Italy (lij_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ligurian, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Ligurian, Italy translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Ligurian, Italy (lij_Latn):
   ```

### `lld_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Ladin, Val Badia, Italy: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Ladin, Val Badia, Italy translator, tasked with providing translations suitable for use in Ladin, Val Badia, Italy (lld_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ladin, Val Badia, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Ladin, Val Badia, Italy translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Ladin, Val Badia, Italy (lld_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Ladin, Val Badia, Italy: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Ladin, Val Badia, Italy translator, tasked with providing translations suitable for use in Ladin, Val Badia, Italy (lld_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ladin, Val Badia, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Ladin, Val Badia, Italy. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Ladin, Val Badia, Italy translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ladin, Val Badia, Italy (lld_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Ladin, Val Badia, Italy: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Ladin, Val Badia, Italy translator, tasked with providing translations suitable for use in Ladin, Val Badia, Italy (lld_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ladin, Val Badia, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Ladin, Val Badia, Italy translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ladin, Val Badia, Italy (lld_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Ladin, Val Badia, Italy: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Ladin, Val Badia, Italy translator, tasked with providing translations suitable for use in Ladin, Val Badia, Italy (lld_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ladin, Val Badia, Italy grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Ladin, Val Badia, Italy translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Ladin, Val Badia, Italy (lld_Latn):
   ```

### `ru`
- Rows: `1000`
- Unique instructions: `1`
- Instruction clusters: `inclusive_gender_slash_formatting` x 1

1. `1000` rows | `inclusive_gender_slash_formatting`
   Russian: gender-inclusive slash forms required for past participles/adjectives; no extra output.

   Raw instruction:

   ```text
   Translate the English text into Russian. Make the gender of the author inclusive by combining both masculine and feminine endings using slashes.
    
    Follow these formatting rules strictly:
    use the slash to separate the masculine and feminine endings 
    1. for past tense verb participles, e.g., "купил/а", "был/а" 
    2. for adjectives, e.g., "рад/а", "должен/жна", "счастливый/ая" "сердитый/ая" 
   
    Only output the translation, with no additional formatting or explanations.  
   
    Example 1: "I am happy that I bought it" -> "Я рад/а, что купил/а это" 
    Example 2: "I never saw or heard it" -> "Я никогда этого не видел/а и не слышал/а об этом" 
   
    TEXT: 
   ```

### `ru_RU`
- Rows: `917`
- Unique instructions: `1`
- Instruction clusters: `simple_code_direction` x 1

1. `917` rows | `simple_code_direction`
   Translate from en to ru_RU.

   Raw instruction:

   ```text
   Translate from en to ru_RU.
   ```

### `rus_Cyrl`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Russian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Russian translator, tasked with providing translations suitable for use in Russian (rus_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Russian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Russian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Russian (rus_Cyrl):
   ```

2. `44` rows | `professional_translator_social_media`
   Russian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Russian translator, tasked with providing translations suitable for use in Russian (rus_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Russian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Russian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Russian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Russian (rus_Cyrl):
   ```

3. `14` rows | `professional_translator_news_html`
   Russian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Russian translator, tasked with providing translations suitable for use in Russian (rus_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Russian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Russian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Russian (rus_Cyrl):
   ```

4. `7` rows | `professional_translator_software_json`
   Russian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Russian translator, tasked with providing translations suitable for use in Russian (rus_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Russian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Russian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Russian (rus_Cyrl):
   ```

### `sme_Latn`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Northern Sámi: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Northern Sámi translator, tasked with providing translations suitable for use in Northern Sámi (sme_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Northern Sámi grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Northern Sámi translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Northern Sámi (sme_Latn):
   ```

2. `44` rows | `professional_translator_social_media`
   Northern Sámi: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Northern Sámi translator, tasked with providing translations suitable for use in Northern Sámi (sme_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Northern Sámi grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Northern Sámi. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Northern Sámi translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Northern Sámi (sme_Latn):
   ```

3. `14` rows | `professional_translator_news_html`
   Northern Sámi: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Northern Sámi translator, tasked with providing translations suitable for use in Northern Sámi (sme_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Northern Sámi grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Northern Sámi translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Northern Sámi (sme_Latn):
   ```

4. `7` rows | `professional_translator_software_json`
   Northern Sámi: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Northern Sámi translator, tasked with providing translations suitable for use in Northern Sámi (sme_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Northern Sámi grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Northern Sámi translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Northern Sámi (sme_Latn):
   ```

### `tha_Thai`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Thai: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Thai translator, tasked with providing translations suitable for use in Thai (tha_Thai). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Thai grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Thai translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Thai (tha_Thai):
   ```

2. `44` rows | `professional_translator_social_media`
   Thai: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Thai translator, tasked with providing translations suitable for use in Thai (tha_Thai). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Thai grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Thai. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Thai translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Thai (tha_Thai):
   ```

3. `14` rows | `professional_translator_news_html`
   Thai: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Thai translator, tasked with providing translations suitable for use in Thai (tha_Thai). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Thai grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Thai translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Thai (tha_Thai):
   ```

4. `7` rows | `professional_translator_software_json`
   Thai: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Thai translator, tasked with providing translations suitable for use in Thai (tha_Thai). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Thai grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Thai translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Thai (tha_Thai):
   ```

### `ukr_Cyrl`
- Rows: `513`
- Unique instructions: `5`
- Instruction clusters: `professional_translator_czech_education_html` x 1, `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `247` rows | `professional_translator_spoken_asr`
   Ukrainian: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Ukrainian translator, tasked with providing translations suitable for use in Ukrainian (ukr_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ukrainian grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Ukrainian translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Ukrainian (ukr_Cyrl):
   ```

2. `117` rows | `professional_translator_social_media`
   Ukrainian: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Ukrainian translator, tasked with providing translations suitable for use in Ukrainian (ukr_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ukrainian grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Ukrainian. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Ukrainian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ukrainian (ukr_Cyrl):
   ```

3. `79` rows | `professional_translator_news_html`
   Ukrainian: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Ukrainian translator, tasked with providing translations suitable for use in Ukrainian (ukr_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ukrainian grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Ukrainian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ukrainian (ukr_Cyrl):
   ```

4. `63` rows | `professional_translator_czech_education_html`
   Ukrainian: Czech educational exercises prompt; preserve HTML.

   Raw instruction:

   ```text
   You are a professional Ukrainian translator, tasked with providing translations suitable for use in Ukrainian (ukr_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ukrainian grammar and vocabulary and ensuring that the translation is natural. The original Czech text consists of biology, chemistry, and geography exercises extracted from an educational web portal for children aged 9-16. Produce only the Ukrainian translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Ukrainian (ukr_Cyrl):
   ```

5. `7` rows | `professional_translator_software_json`
   Ukrainian: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Ukrainian translator, tasked with providing translations suitable for use in Ukrainian (ukr_Cyrl). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Ukrainian grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Ukrainian translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Ukrainian (ukr_Cyrl):
   ```

### `vie_Latn`
- Rows: `315`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_czech_education_html` x 1, `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_spoken_asr` x 1

1. `114` rows | `professional_translator_spoken_asr`
   Vietnamese: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Vietnamese translator, tasked with providing translations suitable for use in Vietnamese (vie_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Vietnamese grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Vietnamese translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Vietnamese (vie_Latn):
   ```

2. `73` rows | `professional_translator_social_media`
   Vietnamese: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Vietnamese translator, tasked with providing translations suitable for use in Vietnamese (vie_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Vietnamese grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Vietnamese. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Vietnamese translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Vietnamese (vie_Latn):
   ```

3. `65` rows | `professional_translator_news_html`
   Vietnamese: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Vietnamese translator, tasked with providing translations suitable for use in Vietnamese (vie_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Vietnamese grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Vietnamese translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Vietnamese (vie_Latn):
   ```

4. `63` rows | `professional_translator_czech_education_html`
   Vietnamese: Czech educational exercises prompt; preserve HTML.

   Raw instruction:

   ```text
   You are a professional Vietnamese translator, tasked with providing translations suitable for use in Vietnamese (vie_Latn). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Vietnamese grammar and vocabulary and ensuring that the translation is natural. The original Czech text consists of biology, chemistry, and geography exercises extracted from an educational web portal for children aged 9-16. Produce only the Vietnamese translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Vietnamese (vie_Latn):
   ```

### `zh_CN`
- Rows: `747`
- Unique instructions: `1`
- Instruction clusters: `simple_code_direction` x 1

1. `747` rows | `simple_code_direction`
   Translate from en to zh_CN.

   Raw instruction:

   ```text
   Translate from en to zh_CN.
   ```

### `zho_Hans`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Chinese, Simplified: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Chinese, Simplified translator, tasked with providing translations suitable for use in Chinese, Simplified (zho_Hans). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Simplified grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Chinese, Simplified translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Chinese, Simplified (zho_Hans):
   ```

2. `44` rows | `professional_translator_social_media`
   Chinese, Simplified: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Chinese, Simplified translator, tasked with providing translations suitable for use in Chinese, Simplified (zho_Hans). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Simplified grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Chinese, Simplified. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Chinese, Simplified translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Chinese, Simplified (zho_Hans):
   ```

3. `14` rows | `professional_translator_news_html`
   Chinese, Simplified: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Chinese, Simplified translator, tasked with providing translations suitable for use in Chinese, Simplified (zho_Hans). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Simplified grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Chinese, Simplified translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Chinese, Simplified (zho_Hans):
   ```

4. `7` rows | `professional_translator_software_json`
   Chinese, Simplified: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Chinese, Simplified translator, tasked with providing translations suitable for use in Chinese, Simplified (zho_Hans). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Simplified grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Chinese, Simplified translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Chinese, Simplified (zho_Hans):
   ```

### `zho_Hant_TW`
- Rows: `198`
- Unique instructions: `4`
- Instruction clusters: `professional_translator_news_html` x 1, `professional_translator_social_media` x 1, `professional_translator_software_json` x 1, `professional_translator_spoken_asr` x 1

1. `133` rows | `professional_translator_spoken_asr`
   Chinese, Traditional Taiwan: spoken/ASR transcript prompt; colloquial flow, omit non-linguistic sounds, sentence-per-line.

   Raw instruction:

   ```text
   You are a professional Chinese, Traditional Taiwan translator, tasked with providing translations suitable for use in Chinese, Traditional Taiwan (zho_Hant_TW). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Traditional Taiwan grammar and vocabulary and ensuring that the translation is natural. The original text is automatically transcribed from spoken language and can contain errors. Maintain the flow and colloquial style of the speaker in the translation. Do not include non-linguistic sounds (e.g. laughter, groans, hesitation sounds, etc.), but do include interjections. If a word is interrupted, either guess the full word if possible or otherwise omit it. Keep foreign words as they are when translating. Produce only the Chinese, Traditional Taiwan translation, without any additional explanations or commentary. Output the text such that each sentence is on a separate line. Please translate the following text into Chinese, Traditional Taiwan (zho_Hant_TW):
   ```

2. `44` rows | `professional_translator_social_media`
   Chinese, Traditional Taiwan: social-media prompt; preserve URLs/handles, translate hashtags naturally, informal style, keep HTML.

   Raw instruction:

   ```text
   You are a professional Chinese, Traditional Taiwan translator, tasked with providing translations suitable for use in Chinese, Traditional Taiwan (zho_Hant_TW). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Traditional Taiwan grammar and vocabulary and ensuring that the translation is natural. The original text is user-generated content from a social media platform. Do not reproduce spelling mistakes. Reproduce marks of expressiveness that communicate meaningful intent (e.g. enthusiasm through capitalisation or elongation) in a way that is natural in Chinese, Traditional Taiwan. Copy URLs and user handles directly rather than translating them. However, translate hashtags as appropriate for the translation to be natural for social media text. Follow the punctuation of the source text as best as possible. Additional punctuation should be added only if not doing so would seriously alter the comprehension of the text. Translate text in an informal style, like close friends talking, even if it changes the original tone. Produce only the Chinese, Traditional Taiwan translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Chinese, Traditional Taiwan (zho_Hant_TW):
   ```

3. `14` rows | `professional_translator_news_html`
   Chinese, Traditional Taiwan: news prompt; formal journalistic style, preserve HTML.

   Raw instruction:

   ```text
   You are a professional Chinese, Traditional Taiwan translator, tasked with providing translations suitable for use in Chinese, Traditional Taiwan (zho_Hant_TW). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Traditional Taiwan grammar and vocabulary and ensuring that the translation is natural. The original text is a news article. Ensure the translation is formal and consistent with journalistic standards. Produce only the Chinese, Traditional Taiwan translation, without any additional explanations or commentary. Maintain the HTML formatting of the original source text. Please translate the following text into Chinese, Traditional Taiwan (zho_Hant_TW):
   ```

4. `7` rows | `professional_translator_software_json`
   Chinese, Traditional Taiwan: software JSON prompt; preserve keys/placeholders and output valid JSON.

   Raw instruction:

   ```text
   You are a professional Chinese, Traditional Taiwan translator, tasked with providing translations suitable for use in Chinese, Traditional Taiwan (zho_Hant_TW). Your goal is to accurately convey the meaning and nuances of the original text while adhering to Chinese, Traditional Taiwan grammar and vocabulary and ensuring that the translation is natural. The original text is from software data. Translate the content of json, without translating keys and placeholders (i.e. copy them rather than translate them). Produce only the Chinese, Traditional Taiwan translation, without any additional explanations or commentary. Produce a valid json output that matches the input format. Please translate the following text into Chinese, Traditional Taiwan (zho_Hant_TW):
   ```

