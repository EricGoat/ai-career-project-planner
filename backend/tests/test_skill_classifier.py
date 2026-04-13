from backend.services.skill_classifier import classify_skills


def test_classify_skills_groups_languages_and_cloud_services():
    result = classify_skills(["Java", "Python", "AWS", "GCP", "Azure"])

    assert result["languages"] == ["Java", "Python"]
    assert result["cloud_services"] == ["AWS", "GCP", "Azure"]


def test_classify_skills_places_unmapped_skills_in_other():
    result = classify_skills(["Stakeholder communication"])

    assert result["other"] == ["Stakeholder communication"]


def test_classify_skills_maps_common_dataset_technical_terms():
    result = classify_skills([
        "HTML5",
        "CloudFormation",
        "Redshift",
        ".NET Core fundamentals",
        "REST APIs",
        "Cypress basics",
        "Kafka",
        "Pandas",
        "NumPy",
    ])

    assert result["languages"] == ["HTML5"]
    assert result["cloud_services"] == ["CloudFormation"]
    assert result["databases"] == ["Redshift"]
    assert result["frameworks"] == [".NET Core fundamentals", "REST APIs", "Cypress basics"]
    assert result["devops"] == ["Kafka"]
    assert result["ai_ml"] == ["Pandas", "NumPy"]
