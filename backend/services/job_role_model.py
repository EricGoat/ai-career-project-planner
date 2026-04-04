import re

from backend.services.job_dataset import load_job_dataset


def extract_job_skills(target_role: str) -> list[str]:
    normalized_target_role = normalize_text(target_role)

    if not normalized_target_role:
        return []

    matching_jobs = find_matching_jobs(normalized_target_role)
    if matching_jobs:
        return collect_unique_skills(matching_jobs)

    return []


def find_matching_jobs(normalized_target_role: str) -> list[dict]:
    dataset = load_job_dataset()

    exact_title_matches = [
        job for job in dataset
        if normalize_text(job.get("Title", "")) == normalized_target_role
    ]
    if exact_title_matches:
        return exact_title_matches

    contains_title_matches = [
        job for job in dataset
        if phrase_matches(normalized_target_role, normalize_text(job.get("Title", "")))
           or phrase_matches(normalize_text(job.get("Title", "")), normalized_target_role)
    ]
    if contains_title_matches:
        return contains_title_matches

    keyword_matches = [
        job for job in dataset
        if any(
            phrase_matches(normalized_target_role, normalize_text(keyword))
            or phrase_matches(normalize_text(keyword), normalized_target_role)
            for keyword in job.get("Keywords", [])
        )
    ]
    return keyword_matches


def collect_unique_skills(matching_jobs: list[dict]) -> list[str]:
    unique_skills: list[str] = []
    seen_skills: set[str] = set()

    for job in matching_jobs:
        for skill in job.get("Skills", []):
            normalized_skill = normalize_text(skill)
            if normalized_skill and normalized_skill not in seen_skills:
                seen_skills.add(normalized_skill)
                unique_skills.append(skill)

    return unique_skills
def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def phrase_matches(phrase: str, text: str) -> bool:
    if not phrase or not text:
        return False

    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text) is not None
