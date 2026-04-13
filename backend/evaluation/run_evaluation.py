import json
import re
from pathlib import Path
from backend.services.job_role_model import extract_job_skills
from backend.services.recommender import rank_missing_skills
from backend.services.skill_gap_analysis import canonicalize_skill, find_skill_gaps


ALIASES = {
    "rest api": "rest apis",
    "restful api": "rest apis",
    "restful apis": "rest apis",
    "matplotlib": "data visualization",
    "seaborn": "data visualization",
    "tableau": "data visualization",
    "power bi": "data visualization",
    "css3": "css",
    "tailwind css": "css",
    "pytorch": "deep learning",
    "tensorflow": "deep learning",
    "llms": "machine learning",
    "snowflake": "data modeling",
    "spark basics": "spark",
    "etl fundamentals": "etl",
    "linux basics": "linux",
    "networking basics": "networking",
}


def clean_skill(skill: str) -> str:
    skill = canonicalize_skill(skill)
    skill = re.sub(r"[()/]", " ", skill)
    skill = re.sub(r"\s+", " ", skill).strip()
    return ALIASES.get(skill, skill)


def evaluate(predicted_skills: list[str], true_skills: list[str]) -> dict[str, float]:
    predicted = {clean_skill(skill) for skill in predicted_skills}
    actual = {clean_skill(skill) for skill in true_skills}

    return {
        "tp": len(predicted & actual),
        "fp": len(predicted - actual),
        "fn": len(actual - predicted)
    }


def f1_score(p: float, r: float) -> float:
    if p + r == 0:
        return 0.0
    return 2 * (p * r) / (p + r)


def run_evaluation():
    path = Path(__file__).resolve().parent.parent / "data" / "evaluation_dataset.json"
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for sample in data:
        job_skills = extract_job_skills(sample["job"])
        gaps = find_skill_gaps(sample["resume"], job_skills)
        ranked_gaps = rank_missing_skills(gaps, job_skills, sample["job"])
        ranked_gaps = ranked_gaps[:len(sample["true_missing_skills"])]

        result = evaluate(ranked_gaps, sample["true_missing_skills"])
        total_tp += result["tp"]
        total_fp += result["fp"]
        total_fn += result["fn"]

    p = total_tp / (total_tp + total_fp) if total_tp + total_fp else 0.0
    r = total_tp / (total_tp + total_fn) if total_tp + total_fn else 0.0

    print("\n=== Skill Gap Evaluation ===")
    print("Precision:", round(p, 3))
    print("Recall:", round(r, 3))
    print("F1:", round(f1_score(p, r), 3))


if __name__ == "__main__":
    run_evaluation()
