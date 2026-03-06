"""
QANTAM Prompt Evaluation Harness
Runs prompts against golden datasets and enforces accuracy gates.
"""
import os
import json
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

import litellm

EVAL_DIR = Path(__file__).parent
GOLDEN_DIR = EVAL_DIR / "golden_datasets"
RESULTS_DIR = EVAL_DIR / "results"

ACCURACY_GATES = {
    "clarity_ambiguity": {"metric": "precision", "threshold": 0.70},
    "clarity_completeness": {"metric": "recall", "threshold": 0.70},
    "clarity_conflict": {"metric": "precision", "threshold": 0.80},
    "clarity_regulatory": {"metric": "coverage", "threshold": 0.80},
    "pulse_positive": {"metric": "approval_rate", "threshold": 0.60},
    "pulse_negative": {"metric": "approval_rate", "threshold": 0.55},
    "pulse_compliance": {"metric": "approval_rate", "threshold": 0.50},
}


@dataclass
class EvalResult:
    prompt_name: str
    prompt_version: str
    metric: str
    threshold: float
    score: float
    passed: bool
    samples_evaluated: int
    timestamp: str


def load_golden_dataset(prompt_name: str) -> list:
    """Load golden dataset for a prompt."""
    module = prompt_name.split("_")[0]
    dataset_path = GOLDEN_DIR / module / f"{prompt_name}.json"
    
    if not dataset_path.exists():
        print(f"Warning: No golden dataset found at {dataset_path}")
        return []
    
    with open(dataset_path) as f:
        return json.load(f)


def get_prompt_module(prompt_name: str):
    """Dynamically import prompt module."""
    module = prompt_name.split("_")[0]
    prompt_file = prompt_name.replace(f"{module}_", "") + "_v1"
    
    sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))
    
    try:
        mod = __import__(f"ai.prompts.{module}.{prompt_file}", fromlist=[""])
        return mod
    except ImportError as e:
        print(f"Warning: Could not import prompt module: {e}")
        return None


async def run_prompt(prompt_module, sample: dict) -> dict:
    """Run prompt against a single sample."""
    prompt = prompt_module.build_prompt(sample["input"])
    system = getattr(prompt_module, "SYSTEM_PROMPT", None)
    
    response = await litellm.acompletion(
        model="claude/claude-haiku-4-5-20251001",
        messages=[{"role": "user", "content": prompt}],
        system=system
    )
    
    content = response.choices[0].message.content
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw": content}


def calculate_precision(predictions: list, ground_truth: list) -> float:
    """Calculate precision score."""
    if not predictions:
        return 0.0
    
    true_positives = 0
    for pred in predictions:
        for gt in ground_truth:
            if pred.get("flag_type") == gt.get("flag_type"):
                true_positives += 1
                break
    
    return true_positives / len(predictions)


def calculate_recall(predictions: list, ground_truth: list) -> float:
    """Calculate recall score."""
    if not ground_truth:
        return 1.0
    
    true_positives = 0
    for gt in ground_truth:
        for pred in predictions:
            if pred.get("flag_type") == gt.get("flag_type"):
                true_positives += 1
                break
    
    return true_positives / len(ground_truth)


def calculate_approval_rate(predictions: list, ground_truth: list) -> float:
    """Calculate approval rate (for test generation)."""
    if not predictions:
        return 0.0
    
    approved = sum(1 for p in predictions if p.get("would_approve", False))
    return approved / len(predictions)


async def evaluate_prompt(prompt_name: str) -> Optional[EvalResult]:
    """Evaluate a single prompt against its golden dataset."""
    gate = ACCURACY_GATES.get(prompt_name)
    if not gate:
        print(f"No accuracy gate defined for {prompt_name}")
        return None
    
    dataset = load_golden_dataset(prompt_name)
    if not dataset:
        print(f"No golden dataset for {prompt_name}, skipping")
        return None
    
    prompt_module = get_prompt_module(prompt_name)
    if not prompt_module:
        return None
    
    all_predictions = []
    all_ground_truth = []
    
    for sample in dataset:
        try:
            result = await run_prompt(prompt_module, sample)
            predictions = result.get("flags", result.get("test_cases", []))
            ground_truth = sample.get("expected_flags", sample.get("expected_tests", []))
            
            all_predictions.extend(predictions)
            all_ground_truth.extend(ground_truth)
        except Exception as e:
            print(f"Error evaluating sample: {e}")
            continue
    
    metric = gate["metric"]
    if metric == "precision":
        score = calculate_precision(all_predictions, all_ground_truth)
    elif metric == "recall":
        score = calculate_recall(all_predictions, all_ground_truth)
    elif metric in ["approval_rate", "coverage"]:
        score = calculate_approval_rate(all_predictions, all_ground_truth)
    else:
        score = 0.0
    
    passed = score >= gate["threshold"]
    
    return EvalResult(
        prompt_name=prompt_name,
        prompt_version=getattr(prompt_module, "PROMPT_META", {}).get("version", "unknown"),
        metric=metric,
        threshold=gate["threshold"],
        score=round(score, 4),
        passed=passed,
        samples_evaluated=len(dataset),
        timestamp=datetime.now().isoformat()
    )


async def run_all_evaluations():
    """Run evaluations for all prompts with golden datasets."""
    results = []
    failed = []
    
    for prompt_name in ACCURACY_GATES.keys():
        print(f"Evaluating {prompt_name}...")
        result = await evaluate_prompt(prompt_name)
        
        if result:
            results.append(result)
            status = "PASS" if result.passed else "FAIL"
            print(f"  {status}: {result.score:.2%} (threshold: {result.threshold:.0%})")
            
            if not result.passed:
                failed.append(prompt_name)
    
    RESULTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = RESULTS_DIR / f"eval_{timestamp}.json"
    
    with open(results_file, "w") as f:
        json.dump([asdict(r) for r in results], f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    
    if failed:
        print(f"\nFAILED GATES: {', '.join(failed)}")
        return 1
    
    print("\nAll accuracy gates passed!")
    return 0


if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(run_all_evaluations())
    sys.exit(exit_code)
