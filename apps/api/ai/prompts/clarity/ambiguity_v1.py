"""
CLARITY Ambiguity Detection Prompt v1
"""

PROMPT_META = {
    "name": "clarity_ambiguity",
    "version": "1.0",
    "task_type": "ambiguity_detection",
    "model_target": "claude-sonnet",
    "accuracy_gate": 0.70,
    "created": "2026-03-04"
}

SYSTEM_PROMPT = """You are a senior QA engineer reviewing software requirements.
Your job: identify ambiguous statements a developer could misinterpret."""

USER_PROMPT_TEMPLATE = """Analyse this requirement for ambiguity:

REQUIREMENT: {requirement_text}

Return JSON with flags array containing: flag_type, flagged_text, explanation, suggested_rewrite, confidence_score.
Return empty flags array if requirement is clear."""


def build_prompt(requirement_text: str) -> str:
    return USER_PROMPT_TEMPLATE.format(requirement_text=requirement_text)
