def find_skill_gaps(resume_skills: list, job_skills: list) -> list:
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)

    missing = list(job_set - resume_set)
    return sorted(missing)