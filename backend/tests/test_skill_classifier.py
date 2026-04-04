from backend.services.skill_classifier import classify_skills


def test_classify_skills_groups_languages_and_cloud_services():
    result = classify_skills(["Java", "Python", "AWS", "GCP", "Azure"])

    assert result["languages"] == ["Java", "Python"]
    assert result["cloud_services"] == ["AWS", "GCP", "Azure"]


def test_classify_skills_places_unmapped_skills_in_other():
    result = classify_skills(["Stakeholder communication"])

    assert result["other"] == ["Stakeholder communication"]
