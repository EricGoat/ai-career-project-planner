from flask import Blueprint, request, jsonify
from backend.services.skill_gap_analysis import find_skill_gaps
from backend.services.skill_classifier import classify_skills
from backend.services.recommender import generate_recommendations

recommendation_bp = Blueprint("recommendation_bp", __name__)

@recommendation_bp.route("", methods=["POST"])
def recommend():
    data = request.get_json()

    resume_skills = data.get("resume_skills", [])
    job_skills = data.get("job_skills", [])

    gaps = find_skill_gaps(resume_skills, job_skills)
    recommendations = generate_recommendations(gaps)

    return jsonify({
        "resume_skill_categories": classify_skills(resume_skills),
        "job_skill_categories": classify_skills(job_skills),
        "missing_skill_categories": classify_skills(gaps),
        "missing_skills": gaps,
        "recommendations": recommendations
    })
