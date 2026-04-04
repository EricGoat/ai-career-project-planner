from backend.services.skill_extractor import SkillExtractor
from backend.utils.skill_dictionary import KNOWN_SKILLS, SKILL_ALIASES

extractor = SkillExtractor(KNOWN_SKILLS, SKILL_ALIASES)


def extract_job_skills(job_text: str) -> list[str]:
    return extractor.extract(job_text)