import spacy

nlp = spacy.load("en_core_web_sm")

KNOWN_SKILLS = [
    "python", "java", "sql", "machine learning", "flask",
    "angular", "data analysis", "nlp", "tensorflow", "pandas"
]

def extract_resume_skills(resume_text: str) -> list:
    text = resume_text.lower()

    found_skills = []
    for skill in KNOWN_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))