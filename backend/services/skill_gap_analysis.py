import re


def find_skill_gaps(resume_skills: list, job_skills: list) -> list:
    resume_set = {canonicalize_skill(skill) for skill in resume_skills}
    job_set = {canonicalize_skill(skill) for skill in job_skills}

    missing = list(job_set - resume_set)
    return sorted(missing)


def canonicalize_skill(skill: str) -> str:
    normalized_skill = re.sub(r"\s+", " ", skill.strip().lower())

    version_control_terms = (
        "git",
        "github",
        "gitlab",
        "version control",
    )
    if any(term in normalized_skill for term in version_control_terms):
        return "git"

    normalized_skill = re.sub(
        r"\b(basics|basic|fundamentals|fundamental|advanced|awareness|familiarity|knowledge)\b",
        "",
        normalized_skill,
    )
    normalized_skill = re.sub(r"\s+", " ", normalized_skill).strip()

    return normalized_skill
