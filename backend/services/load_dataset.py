import json
from pathlib import Path
import re

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "job_dataset.json"

def load_job_dataset() -> list[dict]:
    with DATASET_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def load_skills_dataset() -> list[str]:
    skills = []
    seen = set()

    for job in load_job_dataset():
        for skill in job.get("Skills", []):
            name = skill.strip()
            simple_name = re.sub(
                r"\b(basics|basic|fundamentals|fundamental|advanced|awareness|familiarity|knowledge)\b",
                "",
                name,
                flags=re.IGNORECASE,
            )
            simple_name = re.sub(r"\s+", " ", simple_name).strip(" ,-/")

            for value in [name, simple_name]:
                if value and value.lower() not in seen:
                    seen.add(value.lower())
                    skills.append(value)

    return skills
