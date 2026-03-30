from flask import Blueprint, request, jsonify
from services.resume_parser import extract_resume_skills

resume_bp = Blueprint("resume_bp", __name__)

@resume_bp.route("/parse", methods=["POST"])
def parse_resume():
    data = request.get_json()
    resume_text = data.get("resume_text", "")

    skills = extract_resume_skills(resume_text)

    return jsonify({
        "resume_skills": skills
    })