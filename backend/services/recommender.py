from backend.services.skill_gap_analysis import (
    average_vectors,
    canonicalize_skill,
    cosine_similarity,
    embed_text,
    get_recommendation_embedding_assets,
)


def generate_recommendations(skill_gaps: list[str], job_skills: list[str] | None = None) -> list[dict[str, str]]:
    ranked_skills = rank_missing_skills_by_embedding(skill_gaps, job_skills or [])

    recommendations = []
    for skill in ranked_skills[:5]:
        recommendations.append({
            "skill": skill,
            "project": f"Build a small portfolio project using {skill}",
            "resource": f"Study official documentation or a beginner course for {skill}",
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
