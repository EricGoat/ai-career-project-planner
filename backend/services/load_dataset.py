from functools import lru_cache
import re
import json
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "job_dataset.json"

@lru_cache(maxsize=1)
def load_job_dataset() -> list[dict]:
    with DATASET_PATH.open(encoding="utf-8") as dataset_file:
        return json.load(dataset_file)

@lru_cache(maxsize=1)
def load_skills_dataset() -> list[str]:
    unique_skills: list[str] = []
    seen_skills: set[str] = set()

    for job in load_job_dataset():
        for skill in job.get("Skills", []):
            for skill_variant in expand_skill_variants(skill):
                normalized_skill = skill_variant.strip().lower()
                if normalized_skill and normalized_skill not in seen_skills:
                    seen_skills.add(normalized_skill)
                    unique_skills.append(skill_variant)

    return unique_skills


def expand_skill_variants(skill: str) -> list[str]:
    variants = [skill]
    simplified_skill = re.sub(
        r"\b(basics|basic|fundamentals|fundamental|advanced|awareness|familiarity|knowledge)\b",
        "",
        skill,
        flags=re.IGNORECASE,
    )
    simplified_skill = re.sub(r"\s+", " ", simplified_skill).strip(" ,-/")

    if simplified_skill and simplified_skill.lower() != skill.strip().lower():
        variants.append(simplified_skill)

    return variants
