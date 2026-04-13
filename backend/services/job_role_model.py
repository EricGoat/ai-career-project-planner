import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.services.load_dataset import load_job_dataset

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


def extract_job_skills(target_role: str) -> list[str]:
    target_role = normalize_text(target_role)
    if not target_role:
        return []

    target_role = TITLE_ALIASES.get(target_role, target_role)

    jobs = []
    titles = []
    seen_titles = set()

    for job in load_job_dataset():
        title = normalize_text(job.get("Title", ""))
        if title and title not in seen_titles:
            seen_titles.add(title)
            jobs.append(job)
            titles.append(title)

    if not titles:
        return []

    scores = similarity_scores(target_role, titles)

    best_index = max(range(len(scores)), key=lambda i: scores[i])
    best_score = scores[best_index]
    if best_score <= 0:
        return []

    return jobs[best_index].get("Skills", [])


def similarity_scores(query: str, texts: list[str]) -> list[float]:
    if not texts:
        return []

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([query] + texts)
    scores = cosine_similarity(matrix[0:1], matrix[1:])[0]
    return [float(score) for score in scores]
