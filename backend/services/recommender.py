from urllib.parse import quote_plus
from backend.services.skill_gap_analysis import (
    average_vectors,
    canonicalize_skill,
    cosine_similarity,
    embed_text,
    get_recommendation_embedding_assets,
)
from backend.services.skill_classifier import categorize_skill


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


def generate_recommendations(skill_gaps: list[str], job_skills: list[str] | None = None) -> list[dict[str, str]]:
    ranked_skills = rank_missing_skills_by_embedding(skill_gaps, job_skills or [])

    recommendations = []
    for skill in ranked_skills[:5]:
        category = categorize_skill(skill)
        category_recommendation = CATEGORY_RECOMMENDATIONS[category]
        documentation_link = get_documentation_link(skill)
        recommendations.append({
            "skill": skill,
            "category": category,
            "project": category_recommendation["project"].format(skill=skill),
            "resource": f"Read the official documentation: {documentation_link}",
            "resource_link": documentation_link,
        })

    return recommendations


def rank_missing_skills_by_embedding(skill_gaps: list[str], job_skills: list[str]) -> list[str]:
    if not skill_gaps:
        return []

    if not job_skills:
        return list(skill_gaps)

    assets = get_recommendation_embedding_assets()
    skill_to_index = assets["skill_to_index"]
    context_vectors = assets["context_vectors"]
    text_index = assets["text_index"]

    job_context_vectors = []
    job_text_vectors = []
    for skill in job_skills:
        normalized_skill = canonicalize_skill(skill)
        if normalized_skill in skill_to_index:
            job_context_vectors.append(context_vectors[skill_to_index[normalized_skill]])
        job_text_vectors.append(embed_text(text_index, normalized_skill))

    average_context = average_vectors(job_context_vectors)
    average_text = average_vectors(job_text_vectors)

    scored_skills = []
    for index, skill in enumerate(skill_gaps):
        normalized_skill = canonicalize_skill(skill)
        context_score = 0.0
        if normalized_skill in skill_to_index and average_context.size:
            context_score = cosine_similarity(context_vectors[skill_to_index[normalized_skill]], average_context)

        text_score = cosine_similarity(embed_text(text_index, normalized_skill), average_text)
        final_score = (0.7 * context_score) + (0.3 * text_score)
        scored_skills.append((final_score, -index, skill))

    scored_skills.sort(reverse=True)
    return [skill for _, _, skill in scored_skills]
