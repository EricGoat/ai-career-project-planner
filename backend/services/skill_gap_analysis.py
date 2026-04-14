import re
from backend.services.load_dataset import extract_skills_from_dataset

REMOVE_WORDS_PATTERN = re.compile(
    r"\b(basics|basic|fundamentals|fundamental|advanced|awareness|familiarity|knowledge)\b",
    flags=re.IGNORECASE,
)

SKILL_ALIASES = {
    "github": "git",
    "gitlab": "git",
    "version control": "git",
    "js": "javascript",
    "ts": "typescript",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "py": "python",
}


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s+#.]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def canonicalize_skill(skill: str) -> str:
    skill = normalize_text(skill)
    skill = REMOVE_WORDS_PATTERN.sub("", skill)
    skill = re.sub(r"\s+", " ", skill).strip(" ,-/")
    return SKILL_ALIASES.get(skill, skill)


def find_skill_gaps(resume_skills: list[str], job_skills: list[str]) -> list[str]:
    resume = {canonicalize_skill(skill) for skill in resume_skills if canonicalize_skill(skill)}
    job = {canonicalize_skill(skill) for skill in job_skills if canonicalize_skill(skill)}
    return sorted(job - resume)


def make_skill_index(skills: list[str]) -> dict[str, list[str]]:
    clean_skills = []
    seen = set()

    for skill in skills:
        name = canonicalize_skill(skill)
        if name and name not in seen:
            seen.add(name)
            clean_skills.append(name)

    return {"skills": clean_skills}


def get_resume_skill_index() -> dict[str, list[str]]:
    return make_skill_index(extract_skills_from_dataset())
