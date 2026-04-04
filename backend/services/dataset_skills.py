from functools import lru_cache

from backend.services.job_dataset import load_job_dataset


@lru_cache(maxsize=1)
def load_dataset_skills() -> list[str]:
    unique_skills: list[str] = []
    seen_skills: set[str] = set()

    for job in load_job_dataset():
        for skill in job.get("Skills", []):
            normalized_skill = skill.strip().lower()
            if normalized_skill and normalized_skill not in seen_skills:
                seen_skills.add(normalized_skill)
                unique_skills.append(skill)

    return unique_skills
