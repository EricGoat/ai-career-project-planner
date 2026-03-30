from backend.services.skill_gap_analysis import find_skill_gaps

def test_find_skill_gaps():
    resume_skills = ["python", "sql"]
    job_skills = ["python", "sql", "flask"]

    result = find_skill_gaps(resume_skills, job_skills)

    assert result == ["flask"]