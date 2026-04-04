from functools import lru_cache
import re

from backend.services.job_dataset import load_job_dataset


@lru_cache(maxsize=1)
def load_dataset_skills() -> list[str]:
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
