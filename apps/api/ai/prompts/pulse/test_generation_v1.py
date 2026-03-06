"""
PULSE Test Generation Prompt v1
Generates positive, negative, edge, and compliance test cases.
"""

PROMPT_META = {
    "name": "pulse_test_generation",
    "version": "1.0",
    "task_type": "test_generation",
    "model_target": "claude-haiku",
    "accuracy_gate": 0.60,
    "created": "2026-03-04"
}

SYSTEM_PROMPT = """You are a senior test engineer generating comprehensive test cases.
Use the CLARITY analysis context to focus on areas with quality flags.
Generate tests that would catch the issues flagged by CLARITY.

Test types to generate:
- positive: Happy path scenarios that verify correct behavior
- negative: Invalid inputs, error conditions, boundary violations
- edge: Boundary values, empty states, maximum limits
- compliance: Regulatory requirements (GDPR, PCI-DSS, etc.)
"""

USER_PROMPT_TEMPLATE = """Generate test cases for this requirement:

REQUIREMENT: {requirement_text}

CLARITY FLAGS (focus testing here):
{clarity_flags}

REGULATORY CLAUSES (if any):
{regulatory_clauses}

TEST TYPES TO GENERATE: {test_types}

Return JSON with this exact structure:
{{
  "test_cases": [
    {{
      "title": "descriptive test case title",
      "type": "positive|negative|edge|compliance",
      "preconditions": ["list of preconditions"],
      "steps": ["step 1", "step 2", "step 3"],
      "expected_result": "what should happen",
      "priority": "P0|P1|P2|P3",
      "confidence_score": 0-100
    }}
  ],
  "coverage_notes": "what scenarios are covered",
  "overall_confidence": 0-100
}}

Generate 3-5 test cases per type requested.
Focus on testable, specific scenarios - not vague descriptions.
"""


def build_prompt(
    requirement_text: str,
    clarity_flags: list,
    regulatory_clauses: list,
    test_types: list
) -> str:
    """Build the full prompt for test generation."""
    flags_str = "\n".join([f"- {f['flag_type']}: {f['flagged_text']}" for f in clarity_flags]) or "None"
    regs_str = "\n".join([f"- {r}" for r in regulatory_clauses]) or "None"
    types_str = ", ".join(test_types)
    
    return USER_PROMPT_TEMPLATE.format(
        requirement_text=requirement_text,
        clarity_flags=flags_str,
        regulatory_clauses=regs_str,
        test_types=types_str
    )
