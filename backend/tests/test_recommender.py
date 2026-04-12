import numpy as np
from backend.services import recommender


class FakeTextIndex:
    def __init__(self, mapping):
        self.mapping = mapping

    def __getitem__(self, key):
        return self.mapping[key]


def test_rank_missing_skills_by_embedding_uses_profile_similarity(monkeypatch):
    monkeypatch.setattr(recommender, "embed_text", lambda index, text: np.array(index[text], dtype=np.float32))
    monkeypatch.setattr(
        recommender,
        "get_recommendation_embedding_assets",
        lambda: {
            "skill_to_index": {"flask": 0, "django": 1, "docker": 2, "git": 3},
            "context_vectors": np.array([
                [1.0, 0.0],
                [0.9, 0.1],
                [0.0, 1.0],
                [0.2, 0.8],
            ], dtype=np.float32),
            "text_index": FakeTextIndex({
                "flask": [1.0, 0.0],
                "django": [0.9, 0.1],
                "docker": [0.0, 1.0],
                "git": [0.2, 0.8],
            }),
        },
    )

    result = recommender.rank_missing_skills_by_embedding(["docker", "django", "git"], ["flask"])

    assert result == ["django", "git", "docker"]


def test_get_documentation_link_returns_search_url_when_lookup_fails(monkeypatch):
    result = recommender.get_documentation_link("custom internal tool")

    assert result == "https://google.com/search?q=custom+internal+tool+official+documentation"
