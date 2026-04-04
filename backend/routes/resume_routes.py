from flask import Blueprint, request, jsonify
from backend.services.resume_file_parser import extract_resume_text_from_file
from backend.services.resume_parser import extract_resume_skills

resume_bp = Blueprint("resume_bp", __name__)

@resume_bp.route("/parse", methods=["POST"])
def parse_resume():
    resume_file = request.files.get("resume_file")

    if resume_file is None or resume_file.filename == "":
        return jsonify({"error": "resume_file is required"}), 400

    try:
        resume_text = extract_resume_text_from_file(
            resume_file.read(),
            resume_file.filename
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    skills = extract_resume_skills(resume_text)

    return jsonify({
        "resume_skills": skills
    })
