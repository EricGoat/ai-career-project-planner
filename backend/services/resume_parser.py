from backend.services.skill_extractor import SkillExtractor
from backend.services.dataset_skills import load_dataset_skills

extractor = SkillExtractor(load_dataset_skills())


def extract_resume_skills(resume_text: str) -> list[str]:
    return extractor.extract(resume_text)
