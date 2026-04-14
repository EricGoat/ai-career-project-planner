from urllib.parse import quote_plus
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from backend.services.skill_classifier import categorize_skill
from backend.services.skill_gap_analysis import canonicalize_skill, normalize_text

CATEGORY_RECOMMENDATIONS: dict[str, dict[str, str]] = {
    "languages": {
        "project": "Solve a focused coding challenge and then build a command-line tool with {skill}",
    },
    "cloud_services": {
        "project": "Deploy a small service on {skill} with monitoring and a short architecture write-up",
    },
    "databases": {
        "project": "Design a schema in {skill} and build queries for reporting and CRUD operations",
    },
    "frameworks": {
        "project": "Build a production-style web app feature using {skill} with routing, validation, and tests",
    },
    "devops": {
        "project": "Automate a delivery workflow with {skill} and document the deployment pipeline",
    },
    "version_control": {
        "project": "Create a collaborative repo workflow using {skill} with branches, pull requests, and release tags",
    },
    "ai_ml": {
        "project": "Train and evaluate a small model or prototype using {skill} and summarize the results",
    },
    "other": {
        "project": "Build a small portfolio project that demonstrates {skill} in a realistic workflow",
    }
}


def get_documentation_link(skill: str) -> str:
    return f"https://google.com/search?q={quote_plus(f'{skill} official documentation')}"


def generate_recommendations(
    skill_gaps: list[str],
    job_skills: list[str] | None = None,
    job_context: str | None = None,
) -> list[dict[str, str]]:
    ranked_skills = rank_missing_skills(skill_gaps, job_skills or [], job_context)

    recommendations = []
    for skill in ranked_skills[:5]:
        category = categorize_skill(skill)
        recommendations.append({
            "skill": skill,
            "category": category,
            "project": CATEGORY_RECOMMENDATIONS[category]["project"].format(skill=skill),
            "resource": f"Read the official documentation: {get_documentation_link(skill)}",
            "resource_link": get_documentation_link(skill),
        })

    return recommendations


def cosine_similarity(text1: str, text2: str) -> float:
    text1 = normalize_text(text1).replace(" ", "")
    text2 = normalize_text(text2).replace(" ", "")

    if not text1 or not text2:
        return 0.0

    vectorizer = CountVectorizer(analyzer="char")
    matrix = vectorizer.fit_transform([text1, text2])
    return float(sklearn_cosine_similarity(matrix[0:1], matrix[1:2])[0][0])


def rank_missing_skill_score(skill_gap: str, job_skills: list[str], context: str) -> float:
    gap = canonicalize_skill(skill_gap)
    if not gap:
        return float("-inf")

    normalized_job_skills = [
        canonicalize_skill(skill)
        for skill in job_skills
        if skill and canonicalize_skill(skill) != gap
    ]

    similarities = [
        cosine_similarity(gap, job_skill)
        for job_skill in normalized_job_skills
    ]

    max_sim = max(similarities, default=0.0)
    avg_sim = sum(similarities) / len(similarities) if similarities else 0.0

    context_sim = cosine_similarity(gap, canonicalize_skill(context)) if context else 0.0

    score = 0.7 * max_sim + 0.2 * avg_sim + 0.1 * context_sim

    return score


def rank_missing_skills(
    skill_gaps: list[str],
    job_skills: list[str],
    job_context: str | None = None,
) -> list[str]:
    if not skill_gaps:
        return []

    if not job_skills:
        return list(skill_gaps)

    context = job_context or " ".join(canonicalize_skill(skill) for skill in job_skills if skill)
    ranked = []
    for i, skill in enumerate(skill_gaps):
        score = rank_missing_skill_score(skill, job_skills, context)
        ranked.append((score, -i, skill))

    ranked.sort(reverse=True)
    return [skill for _, _, skill in ranked]
