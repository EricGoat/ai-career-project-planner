from flask import Blueprint, request, jsonify
from services.job_role_model import extract_job_skills

job_bp = Blueprint("job_bp", __name__)

@job_bp.route("/analyze", methods=["POST"])
def analyze_job():
    data = request.get_json()
    job_text = data.get("job_text", "")

    skills = extract_job_skills(job_text)

    return jsonify({
        "job_skills": skills
    })