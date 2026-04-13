import re
from backend.services.skill_gap_analysis import get_resume_skill_embedding_index, normalize_embedding_text


class SkillExtractor:
    def __init__(self, skills, aliases=None, embedding_index=None):
        self.skills = []
        self.aliases = {}

        for skill in skills:
            name = normalize_embedding_text(skill)
            if name and name not in self.skills:
                self.skills.append(name)

        for alias, target in (aliases or {}).items():
            self.aliases[normalize_embedding_text(alias)] = normalize_embedding_text(target)

        if embedding_index is None:
            self.embedding_index = {"skills": self.skills, "aliases": self.aliases}
        else:
            self.embedding_index = embedding_index

    def extract(self, text: str) -> list[str]:
        text = normalize_embedding_text(text)
        found = []
        words = text.split()

        for skill in self.skills:
            if re.search(rf"\b{re.escape(skill)}\b", text) and skill not in found:
                found.append(skill)

        for alias, target in self.aliases.items():
            if re.search(rf"\b{re.escape(alias)}\b", text) and target not in found:
                found.append(target)

        for i in range(len(words) - 1):
            phrase = words[i] + " " + words[i + 1]
            simple_phrase = phrase.replace(" ", "")
            for skill in self.skills:
                if simple_phrase == skill.replace(" ", "") and skill not in found:
                    found.append(skill)

        found.sort()
        return found


def default_skill_extractor() -> SkillExtractor:
    index = get_resume_skill_embedding_index()
    return SkillExtractor(index["skills"], index["aliases"], index)
