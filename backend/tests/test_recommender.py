from backend.services import recommender


def test_rank_missing_skills_by_embedding_prefers_concrete_backend_skills():
    result = recommender.rank_missing_skills(
        ["GraphQL", "Spring Boot", "Windows Server"],
        ["flask", "django", "git"],
        "Backend Developer"
    )

    assert result[0] == "Spring Boot"


def test_rank_missing_skills_by_embedding_uses_job_context_for_ranking():
    result = recommender.rank_missing_skills(
        ["GraphQL", "RESTful API", "Windows Server"],
        ["REST APIs", "Node.js", "Git"],
        "Backend Developer"
    )

    assert result[0] == "RESTful API"


def test_get_documentation_link_returns_search_url_when_lookup_fails():
    result = recommender.get_documentation_link("custom internal tool")

    assert result == "https://google.com/search?q=custom+internal+tool+official+documentation"
