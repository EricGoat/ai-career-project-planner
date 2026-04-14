import re
import json
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "job_dataset.json"


def load_job_dataset() -> list[dict]:
    with DATASET_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def extract_skills_from_dataset() -> list[str]:
    jobs = load_job_dataset()
    skills = []
    seen = set()

    for job in jobs:
        for skill in job.get("Skills", []):
            skill = normalize_skill_name(skill)

            if skill not in seen:
                seen.add(skill)
                skills.append(skill)

    return skills


def normalize_skill_name(skill: str) -> str:
    skill = re.sub(
        r"\b(basics|basic|fundamentals|fundamental|advanced|awareness|familiarity|knowledge)\b",
        "",
        skill.strip(),
        flags=re.IGNORECASE,
    )
    skill = re.sub(r"\s+", " ", skill).strip(" ,-/")
    return skill