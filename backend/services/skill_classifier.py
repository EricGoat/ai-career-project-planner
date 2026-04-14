import re
from backend.services.skill_gap_analysis import canonicalize_skill

SKILL_CATEGORY_PATTERNS = {
    "languages": [
        "python", "java", "javascript", "typescript", "c#", "c++", "go", "ruby", "php",
        "swift", "kotlin", "scala", "rust", "r", "sql", "html", "css", "html5", "css3",
        "bash", "powershell", "vb.net", "objective-c",
    ],
    "cloud_services": [
        "aws", "azure", "gcp", "google cloud", "ec2", "s3", "lambda", "bigquery",
        "cloudformation", "iam",
    ],
    "databases": [
        "mysql", "postgresql", "postgres", "mongodb", "redis", "sql server", "oracle",
        "dynamodb", "firebase", "snowflake", "nosql", "cassandra", "sqlite", "redshift",
    ],
    "frameworks": [
        "react", "react.js", "angular", "vue", "vue.js", "flask", "django", "fastapi",
        "spring", "spring boot", "asp.net", "asp.net mvc", ".net", ".net framework",
        ".net core", "node.js", "express", "express.js", "next.js", "entity framework",
        "mvc", "razor", "graphql", "rest api", "rest apis", "restful api", "microservices",
        "mvvm", "webpack", "babel", "npm", "yarn", "postman", "selenium", "cypress",
        "jmeter", "appium", "testng", "nunit", "junit", "unit testing",
    ],
    "devops": [
        "docker", "kubernetes", "terraform", "jenkins", "ci/cd", "ansible", "helm",
        "prometheus", "grafana", "linux", "hadoop", "spark", "kafka", "flink",
        "docker swarm",
    ],
    "version_control": ["git", "github", "gitlab", "bitbucket", "version control"],
    "ai_ml": [
        "machine learning", "deep learning", "nlp", "computer vision", "tensorflow",
        "pytorch", "scikit-learn", "llm", "llms", "transformers", "keras", "pandas",
        "numpy", "matplotlib", "seaborn", "hugging face", "reinforcement learning",
        "predictive modeling", "classification", "regression", "forecasting",
        "feature engineering",
    ],
}


def categorize_skill(skill: str) -> str:
    skill = canonicalize_skill(skill)

    for category, words in SKILL_CATEGORY_PATTERNS.items():
        for word in words:
            if re.search(rf"\b{re.escape(word)}\b", skill):
                return category

    return "other"


def classify_skills(skills: list[str]) -> dict[str, list[str]]:
    result = {category: [] for category in SKILL_CATEGORY_PATTERNS}
    result["other"] = []

    for skill in skills:
        category = categorize_skill(skill)
        if skill not in result[category]:
            result[category].append(skill)

    return result
