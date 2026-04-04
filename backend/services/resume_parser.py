from backend.services.skill_extractor import SkillExtractor
from backend.utils.skill_dictionary import KNOWN_SKILLS, SKILL_ALIASES

extractor = SkillExtractor(KNOWN_SKILLS, SKILL_ALIASES)


def extract_resume_skills(resume_text: str) -> list[str]:
    return extractor.extract(resume_text)