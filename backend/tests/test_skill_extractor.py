from backend.services.skill_extractor import SkillExtractor

skills = ["python", "machine learning", "javascript"]
aliases = {"ml": "machine learning", "js": "javascript"}


def test_extract_direct_skill():
    extractor = SkillExtractor(skills, aliases)
    text = "Experienced in Python and machine learning."
    assert extractor.extract(text) == ["machine learning", "python"]


def test_extract_alias_skill():
    extractor = SkillExtractor(skills, aliases)
    text = "Worked with JS and ML in several projects."
    assert extractor.extract(text) == ["javascript", "machine learning"]


def test_extract_no_duplicates():
    extractor = SkillExtractor(skills, aliases)
    text = "Python, python, and PYTHON"
    assert extractor.extract(text) == ["python"]