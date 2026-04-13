import re


def canonicalize_skill(skill: str) -> str:
    skill = skill.strip().lower()
    skill = re.sub(r"\s+", " ", skill)

    if "github" in skill or "gitlab" in skill or "version control" in skill or skill == "git":
        return "git"

    remove_words = ["basics", "basic", "fundamentals", "fundamental", "advanced", "awareness", "familiarity", "knowledge"]
    for word in remove_words:
        skill = skill.replace(word, "")

    skill = re.sub(r"\s+", " ", skill).strip(" ,-/")
    return skill


def find_skill_gaps(resume_skills: list, job_skills: list) -> list:
    resume = set()
    job = set()

    for skill in resume_skills:
        name = canonicalize_skill(skill)
        if name:
            resume.add(name)

    for skill in job_skills:
        name = canonicalize_skill(skill)
        if name:
            job.add(name)

    return sorted(job - resume)


def normalize_embedding_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s+#.]", " ", text)
    return re.sub(r"\s+", " ", text)


def make_skill_embedding_index(skills: list[str], aliases: dict[str, str] | None = None) -> dict:
    clean_skills = []
    for skill in skills:
        name = normalize_embedding_text(skill)
        if name and name not in clean_skills:
            clean_skills.append(name)

    clean_aliases = {}
    for alias, target in (aliases or {}).items():
        clean_aliases[normalize_embedding_text(alias)] = normalize_embedding_text(target)

    return {"skills": clean_skills, "aliases": clean_aliases}


def get_resume_skill_embedding_index() -> dict:
    from backend.services.load_dataset import load_skills_dataset

    aliases = {
        "js": "javascript",
        "ts": "typescript",
        "ml": "machine learning",
        "ai": "artificial intelligence",
        "py": "python",
    }
    return make_skill_embedding_index(load_skills_dataset(), aliases)
