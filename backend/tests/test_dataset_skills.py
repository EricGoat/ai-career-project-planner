from backend.services.load_dataset import load_skills_dataset


def test_load_dataset_skills_uses_job_dataset():
    skills = load_skills_dataset()

    assert skills
    assert "C#" in skills
    assert "SQL Server" in skills
    assert "PHP" in skills
