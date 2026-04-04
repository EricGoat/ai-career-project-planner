import json
from functools import lru_cache
from pathlib import Path


DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "job_dataset.json"


@lru_cache(maxsize=1)
def load_job_dataset() -> list[dict]:
    with DATASET_PATH.open(encoding="utf-8") as dataset_file:
        return json.load(dataset_file)
