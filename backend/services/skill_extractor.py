import re
from backend.services.skill_gap_analysis import canonicalize_skill, get_resume_skill_index

ALLOWED_SINGLE_WORD_SKILLS = {
    "python",
    "java",
    "sql",
    "excel",
    "git",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "tensorflow",
    "pytorch",
    "tableau",
    "react",
    "angular",
    "flask",
    "django",
    "pandas",
    "numpy",
}


class SkillExtractor:
    def __init__(self, skills: list[str]):
        self.skills = sorted(set(canonicalize_skill(skill) for skill in skills if canonicalize_skill(skill)))

        self.multiword_skills = [skill for skill in self.skills if " " in skill]
        self.single_word_skills = [
            skill for skill in self.skills
            if " " not in skill and skill in ALLOWED_SINGLE_WORD_SKILLS
        ]

    def extract(self, text: str) -> list[str]:
        normalized_text = canonicalize_skill(text)
        if not normalized_text:
            return []

        found = set()

        for skill in self.multiword_skills:
            if self._contains(normalized_text, skill):
                found.add(skill)

        for skill in self.single_word_skills:
            if self._contains(normalized_text, skill):
                found.add(skill)

        return sorted(found)

    def _contains(self, text: str, phrase: str) -> bool:
        return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def default_skill_extractor() -> SkillExtractor:
    index = get_resume_skill_index()
    return SkillExtractor(index["skills"])