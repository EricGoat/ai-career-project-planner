from backend.services.load_dataset import load_job_dataset
from backend.services.job_role_model import extract_job_skills


def test_load_job_dataset():
    dataset = load_job_dataset()

    assert isinstance(dataset, list)
    assert dataset
    assert "Title" in dataset[0]
    assert "Skills" in dataset[0]


def test_extract_job_skills_returns_dataset_skills_for_matching_role():
    skills = extract_job_skills(".NET Developer")

    assert skills
    assert "C#" in skills
    assert "ASP.NET" in skills or "ASP.NET MVC" in skills


def test_extract_job_skills_returns_no_matches_for_non_technical_role():
    assert extract_job_skills("dentist") == []


def test_extract_job_skills_maps_backend_engineer_to_backend_role_family():
    skills = extract_job_skills("Backend Engineer")

    assert skills
    assert "Node.js" in skills
