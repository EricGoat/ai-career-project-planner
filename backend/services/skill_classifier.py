import re


SKILL_CATEGORY_PATTERNS: dict[str, tuple[str, ...]] = {
    "languages": (
        "python",
        "java",
        "javascript",
        "typescript",
        "c#",
        "c++",
        "go",
        "ruby",
        "php",
        "swift",
        "kotlin",
        "scala",
        "rust",
        "r",
        "sql",
    ),
    "cloud_services": (
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "ec2",
        "s3",
        "lambda",
        "cloudwatch",
        "azure devops",
        "azure functions",
        "bigquery",
        "cloud run",
        "cloud functions",
    ),
    "databases": (
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "redis",
        "sql server",
        "oracle",
        "dynamodb",
        "firebase",
        "snowflake",
    ),
    "frameworks": (
        "react",
        "angular",
        "vue",
        "flask",
        "django",
        "fastapi",
        "spring",
        "asp.net",
        ".net",
        "node.js",
        "express",
        "next.js",
    ),
    "devops": (
        "docker",
        "kubernetes",
        "terraform",
        "jenkins",
        "ci/cd",
        "ansible",
        "helm",
        "prometheus",
        "grafana",
    ),
    "version_control": (
        "git",
        "github",
        "gitlab",
        "bitbucket",
        "version control",
    ),
    "ai_ml": (
        "machine learning",
        "deep learning",
        "nlp",
        "computer vision",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "llm",
        "transformers",
    ),
}


def classify_skills(skills: list[str]) -> dict[str, list[str]]:
    categorized_skills: dict[str, list[str]] = {
        category: []
        for category in SKILL_CATEGORY_PATTERNS
    }
    categorized_skills["other"] = []

    seen_by_category: dict[str, set[str]] = {
        category: set()
        for category in categorized_skills
    }

    for skill in skills:
        category = categorize_skill(skill)
        normalized_skill = normalize_skill(skill)

        if normalized_skill not in seen_by_category[category]:
            seen_by_category[category].add(normalized_skill)
            categorized_skills[category].append(skill)

    return categorized_skills


def categorize_skill(skill: str) -> str:
    normalized_skill = normalize_skill(skill)

    for category, patterns in SKILL_CATEGORY_PATTERNS.items():
        if any(pattern_matches(pattern, normalized_skill) for pattern in patterns):
            return category

    return "other"


def pattern_matches(pattern: str, skill: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(pattern)}(?!\w)", skill) is not None


def normalize_skill(skill: str) -> str:
    normalized_skill = skill.strip().lower()
    normalized_skill = re.sub(r"\s+", " ", normalized_skill)
    return normalized_skill
