#!/usr/bin/env python3
"""Structural alignment checks for candidate hypotheses."""

from __future__ import annotations

import json
import re
from typing import Any


def parse_json(text: str):
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip(), flags=re.I)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",\s*([}\]])", r"\1", text))


def json_count(text: str) -> int | str:
    try:
        data = parse_json(text)
    except json.JSONDecodeError:
        return "invalid_json"
    return len(data) if isinstance(data, (dict, list)) else 1


def html_p_count(text: str) -> int:
    return text.count("<p>")


def check_structure(source_text: str, hypothesis_text: str) -> dict[str, Any]:
    source_text = (source_text or "").strip()
    hypothesis_text = (hypothesis_text or "").strip()

    if source_text.startswith("```json"):
        source_metric = json_count(source_text)
        hypo_metric = json_count(hypothesis_text)
        return {
            "kind": "json",
            "source_metric": source_metric,
            "hypothesis_metric": hypo_metric,
            "passed": bool(source_metric == hypo_metric),
        }

    if source_text.startswith("<p>"):
        source_metric = html_p_count(source_text)
        hypo_metric = html_p_count(hypothesis_text)
        return {
            "kind": "html",
            "source_metric": source_metric,
            "hypothesis_metric": hypo_metric,
            "passed": bool(source_metric == hypo_metric),
        }

    return {
        "kind": "unstructured",
        "source_metric": None,
        "hypothesis_metric": None,
        "passed": True,
    }
