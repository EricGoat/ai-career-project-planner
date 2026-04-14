from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile
from backend.services.skill_extractor import default_skill_extractor

WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def extract_resume_text_from_file(file_bytes: bytes, filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension in {".txt", ".md"}:
        try:
            return file_bytes.decode("utf-8").strip()
        except UnicodeDecodeError:
            return file_bytes.decode("latin-1").strip()

    if extension == ".docx":
        try:
            with ZipFile(BytesIO(file_bytes)) as archive:
                xml = archive.read("word/document.xml")
        except (BadZipFile, KeyError) as exc:
            raise ValueError("Invalid .docx resume file.") from exc

        root = ElementTree.fromstring(xml)
        text_nodes = root.findall(".//w:t", WORD_NAMESPACE)
        parts = [node.text for node in text_nodes if node.text is not None]
        return " ".join(parts).strip()

    raise ValueError("Unsupported resume file type. Use .txt, .md, or .docx.")


def extract_resume_skills(resume_text: str) -> list[str]:
    skill_extractor = default_skill_extractor()
    return skill_extractor.extract(resume_text)
