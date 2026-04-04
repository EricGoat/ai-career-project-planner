import re
from typing import Iterable

import spacy


def _normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s+#.]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


class SkillExtractor:
    def __init__(self, skills: Iterable[str], aliases: dict[str, str] | None = None):
        self.nlp = spacy.load("en_core_web_sm")

        self.skills = sorted({_normalize_text(skill) for skill in skills})

        self.aliases = {
            _normalize_text(alias): _normalize_text(target)
            for alias, target in (aliases or {}).items()
        }

        self.skill_patterns = {
            skill: re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
            for skill in self.skills
        }

        self.alias_patterns = {
            alias: re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
            for alias in self.aliases
        }

    def extract(self, text: str) -> list[str]:
        normalized_text = _normalize_text(text)
        found = set()

        for skill, pattern in self.skill_patterns.items():
            if pattern.search(normalized_text):
                found.add(skill)

        for alias, pattern in self.alias_patterns.items():
            if pattern.search(normalized_text):
                found.add(self.aliases[alias])

        doc = self.nlp(text)
        for chunk in doc.noun_chunks:
            chunk_text = _normalize_text(chunk.text)
            if chunk_text in self.skills:
                found.add(chunk_text)
            elif chunk_text in self.aliases:
                found.add(self.aliases[chunk_text])

        return sorted(found)

