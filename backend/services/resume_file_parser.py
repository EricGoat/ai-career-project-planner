from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile
from backend.services.skill_extractor import default_skill_extractor


def extract_resume_text_from_file(file_bytes: bytes, filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension == ".txt" or extension == ".md":
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1")

    if extension == ".docx":
        try:
            with ZipFile(BytesIO(file_bytes)) as archive:
                xml = archive.read("word/document.xml")
        except (BadZipFile, KeyError) as exc:
            raise ValueError("Invalid .docx resume file.") from exc

        root = ElementTree.fromstring(xml)
        parts = []
        for node in root.iter():
            if node.text:
                parts.append(node.text)
        return " ".join(parts)

    raise ValueError("Unsupported resume file type. Use .txt, .md, or .docx.")


def extract_resume_skills(resume_text: str) -> list[str]:
    return default_skill_extractor().extract(resume_text)
