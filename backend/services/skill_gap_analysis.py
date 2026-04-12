from functools import lru_cache
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from backend.services.load_dataset import load_job_dataset, load_skills_dataset


def find_skill_gaps(resume_skills: list, job_skills: list) -> list:
    resume_set = {canonicalize_skill(skill) for skill in resume_skills}
    job_set = {canonicalize_skill(skill) for skill in job_skills}
    return sorted(job_set - resume_set)


def canonicalize_skill(skill: str) -> str:
    normalized_skill = re.sub(r"\s+", " ", skill.strip().lower())

    if any(term in normalized_skill for term in ("git", "github", "gitlab", "version control")):
        return "git"

    normalized_skill = re.sub(
        r"\b(basics|basic|fundamentals|fundamental|advanced|awareness|familiarity|knowledge)\b",
        "",
        normalized_skill,
    )
    return re.sub(r"\s+", " ", normalized_skill).strip()


def normalize_embedding_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s+#.]", " ", text)
    return re.sub(r"\s+", " ", text)


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    if left.size == 0 or right.size == 0:
        return 0.0

    left_norm = np.linalg.norm(left)
    right_norm = np.linalg.norm(right)
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0

    return float(np.dot(left, right) / (left_norm * right_norm))


def normalize_vector(vector: np.ndarray) -> np.ndarray:
    vector = np.asarray(vector, dtype=np.float32)
    norm = np.linalg.norm(vector)
    if norm == 0.0:
        return vector
    return vector / norm


def average_vectors(vectors: list[np.ndarray]) -> np.ndarray:
    if not vectors:
        return np.zeros(0, dtype=np.float32)
    return normalize_vector(np.mean(np.asarray(vectors, dtype=np.float32), axis=0))


def make_skill_embedding_index(skills: list[str], aliases: dict[str, str] | None = None) -> dict[str, object]:
    normalized_skills = sorted({normalize_embedding_text(skill) for skill in skills if skill.strip()})
    normalized_aliases = {
        normalize_embedding_text(alias): normalize_embedding_text(target)
        for alias, target in (aliases or {}).items()
    }

    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
    vectorizer.fit(normalized_skills + list(normalized_aliases) or ["skill"])
    temp_index = {"vectorizer": vectorizer}
    skill_vectors = embed_texts(temp_index, normalized_skills)

    return {
        "skills": normalized_skills,
        "aliases": normalized_aliases,
        "vectorizer": vectorizer,
        "skill_vectors": np.asarray(skill_vectors, dtype=np.float32),
    }


def embed_text(index: dict[str, object], text: str) -> np.ndarray:
    vectors = embed_texts(index, [text])
    if len(vectors) == 0:
        return np.zeros(0, dtype=np.float32)
    return vectors[0]


def embed_texts(index: dict[str, object], texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, 0), dtype=np.float32)

    normalized_texts = [normalize_embedding_text(text) for text in texts]
    vectorizer: TfidfVectorizer = index["vectorizer"]
    matrix = vectorizer.transform(normalized_texts).toarray().astype(np.float32)

    for row_index in range(len(matrix)):
        matrix[row_index] = normalize_vector(matrix[row_index])

    return matrix


def find_similar_skills(index: dict[str, object], candidates: list[str], threshold: float = 0.72) -> set[str]:
    matches: set[str] = set()
    skills: list[str] = index["skills"]
    skill_vectors: np.ndarray = index["skill_vectors"]
    if not candidates or len(skill_vectors) == 0:
        return matches

    candidate_vectors = embed_texts(index, candidates)
    similarity_matrix = candidate_vectors @ skill_vectors.T

    for row in similarity_matrix:
        best_index = int(np.argmax(row))
        if float(row[best_index]) >= threshold:
            matches.add(skills[best_index])

    return matches


@lru_cache(maxsize=1)
def get_resume_skill_embedding_index() -> dict[str, object]:
    aliases = {
        "js": "javascript",
        "ts": "typescript",
        "ml": "machine learning",
        "ai": "artificial intelligence",
        "py": "python",
    }
    return make_skill_embedding_index(load_skills_dataset(), aliases)


@lru_cache(maxsize=1)
def get_recommendation_embedding_assets() -> dict[str, object]:
    dataset = load_job_dataset()
    skill_names: list[str] = []
    skill_to_index: dict[str, int] = {}
    job_skill_lists: list[list[str]] = []

    for job in dataset:
        job_skills = sorted({
            canonicalize_skill(skill)
            for skill in job.get("Skills", [])
            if canonicalize_skill(skill)
        })
        job_skill_lists.append(job_skills)

        for skill in job_skills:
            if skill not in skill_to_index:
                skill_to_index[skill] = len(skill_names)
                skill_names.append(skill)

    context_vectors = np.zeros((len(skill_names), len(dataset)), dtype=np.float32)
    for job_index, job_skills in enumerate(job_skill_lists):
        for skill in job_skills:
            context_vectors[skill_to_index[skill], job_index] = 1.0

    for row_index in range(len(skill_names)):
        context_vectors[row_index] = normalize_vector(context_vectors[row_index])

    return {
        "skill_to_index": skill_to_index,
        "context_vectors": context_vectors,
        "text_index": make_skill_embedding_index(skill_names),
    }
