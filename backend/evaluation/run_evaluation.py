import json
from pathlib import Path
from collections import defaultdict
from backend.services.job_role_model import extract_job_skills
from backend.services.recommender import rank_missing_skills
from backend.services.resume_file_parser import extract_resume_skills
from backend.services.skill_gap_analysis import canonicalize_skill, find_skill_gaps

def normalize_skill_list(skills: list[str]) -> set[str]:
    normalized = set()
    for skill in skills:
        name = canonicalize_skill(skill)
        if name:
            normalized.add(name)
    return normalized

def evaluate_prediction(predicted_skills: list[str], true_skills: list[str]) -> dict[str, int]:
    predicted = normalize_skill_list(predicted_skills)
    actual = normalize_skill_list(true_skills)

    tp = len(predicted & actual)
    fp = len(predicted - actual)
    fn = len(actual - predicted)

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }

def empty_bucket() -> dict[str, int]:
    return {
        "samples": 0,
        "tp": 0,
        "fp": 0,
        "fn": 0,
    }

def update_bucket(bucket: dict[str, int], result: dict[str, int]) -> None:
    bucket["samples"] += 1
    bucket["tp"] += result["tp"]
    bucket["fp"] += result["fp"]
    bucket["fn"] += result["fn"]

def summarize_bucket(bucket: dict[str, int]) -> dict[str, float]:
    tp = bucket["tp"]
    fp = bucket["fp"]
    fn = bucket["fn"]

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    return {
        "samples": bucket["samples"],
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }

def print_summary(label: str, summary: dict[str, float]) -> None:
    print(f"\n=== {label} ===")
    print(f"Samples: {summary['samples']}")
    print(f"Precision: {summary['precision']:.3f}")
    print(f"Recall:    {summary['recall']:.3f}")
    print(f"F1:        {summary['f1']:.3f}")

def run_evaluation(top_k: int = 5) -> None:
    path = Path(__file__).resolve().parent.parent / "data" / "evaluation_dataset.json"
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    buckets = defaultdict(empty_bucket)
    buckets["total"] = empty_bucket()

    for sample in data:
        difficulty = sample["difficulty"]

        resume_skills = extract_resume_skills(sample["resume_text"])
        job_skills = extract_job_skills(sample["job"])
        gaps = find_skill_gaps(resume_skills, job_skills)
        ranked_gaps = rank_missing_skills(gaps, job_skills, sample["job"])[:top_k]

        result = evaluate_prediction(ranked_gaps, sample["true_missing_skills"])

        update_bucket(buckets[difficulty], result)
        update_bucket(buckets["total"], result)

    for level in ["easy", "medium", "hard", "total"]:
        summary = summarize_bucket(buckets[level])
        print_summary(level.upper(), summary)

if __name__ == "__main__":
    run_evaluation(top_k=5)