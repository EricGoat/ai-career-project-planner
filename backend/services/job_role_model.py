import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.services.load_dataset import load_job_dataset
from backend.services.skill_gap_analysis import canonicalize_skill

TITLE_ALIASES = {
    "backend engineer": "backend developer",
    "frontend engineer": "frontend developer",
    "systems engineer": "system engineer",
    "database engineer": "data engineer",
    "analytics engineer": "bi analyst",
    "ml engineer": "machine learning engineer",
}


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("-", " ")
    return re.sub(r"\s+", " ", text)


def get_jobs_and_titles() -> tuple[list[dict], list[str]]:
    all_jobs = load_job_dataset()
    jobs = []
    titles = []
    seen_titles = set()

    for job in all_jobs:
        title = normalize_text(job.get("Title", ""))
        if title not in seen_titles:
            seen_titles.add(title)
            jobs.append(job)
            titles.append(title)

    return jobs, titles


def get_title_model():
    jobs, titles = get_jobs_and_titles()
    vectorizer = TfidfVectorizer()
    title_matrix = vectorizer.fit_transform(titles)
    return jobs, titles, vectorizer, title_matrix


def extract_job_skills(target_role: str) -> list[str]:
    target_role = normalize_text(target_role)
    if not target_role:
        return []

    target_role = TITLE_ALIASES.get(target_role, target_role)

    jobs, titles, vectorizer, title_matrix = get_title_model()
    if not titles:
        return []

    query_vector = vectorizer.transform([target_role])
    scores = cosine_similarity(query_vector, title_matrix)[0]

    best_index = max(range(len(scores)), key=lambda i: scores[i])
    best_score = float(scores[best_index])

    if best_score < 0.2:
        return []

    raw_skills = jobs[best_index].get("Skills", [])

    canonical_skills = []
    seen = set()
    for skill in raw_skills:
        name = canonicalize_skill(skill)
        if name not in seen:
            seen.add(name)
            canonical_skills.append(name)

    return canonical_skills
