def generate_recommendations(skill_gaps: list) -> list:
    recommendations = []

    for skill in skill_gaps:
        recommendations.append({
            "skill": skill,
            "project": f"Build a small portfolio project using {skill}",
            "resource": f"Study official documentation or a beginner course for {skill}"
        })

    return recommendations