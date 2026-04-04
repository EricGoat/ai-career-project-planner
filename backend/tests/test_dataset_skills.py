from backend.services.dataset_skills import load_dataset_skills


def test_load_dataset_skills_uses_job_dataset():
    skills = load_dataset_skills()

    assert skills
    assert "C#" in skills
    assert "SQL Server" in skills
