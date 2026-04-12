import re
from typing import Iterable

from backend.services.skill_gap_analysis import (
    find_similar_skills,
    get_resume_skill_embedding_index,
    make_skill_embedding_index,
    normalize_embedding_text,
)


def normalize_text(text: str) -> str:
    return normalize_embedding_text(text)


class SkillExtractor:
    def __init__(self, skills: Iterable[str], aliases: dict[str, str] | None = None, embedding_index=None):
        self.skills = sorted({normalize_text(skill) for skill in skills if skill.strip()})
        self.aliases = {
            normalize_text(alias): normalize_text(target)
            for alias, target in (aliases or {}).items()
        }
        self.embedding_index = embedding_index or make_skill_embedding_index(self.skills, self.aliases)

    def extract(self, text: str) -> list[str]:
        normalized_text = normalize_text(text)
        found = set()

        for skill in self.skills:
            if re.search(rf"\b{re.escape(skill)}\b", normalized_text):
                found.add(skill)

        for alias, target in self.aliases.items():
            if re.search(rf"\b{re.escape(alias)}\b", normalized_text):
                found.add(target)

        found.update(find_similar_skills(self.embedding_index, collect_embedding_candidates(text)))
        return sorted(found)


def collect_embedding_candidates(text: str) -> list[str]:
    pieces: list[str] = []
    tokens = re.findall(r"[A-Za-z0-9+#.]+", text)
    normalized_tokens = [normalize_text(token) for token in tokens if normalize_text(token)]

    for start_index in range(len(normalized_tokens)):
        for size in range(1, 5):
            end_index = start_index + size
            if end_index <= len(normalized_tokens):
                pieces.append(" ".join(normalized_tokens[start_index:end_index]))

    return list(dict.fromkeys(pieces))


def default_skill_extractor() -> SkillExtractor:
    embedding_index = get_resume_skill_embedding_index()
    return SkillExtractor(embedding_index["skills"], embedding_index["aliases"], embedding_index)
