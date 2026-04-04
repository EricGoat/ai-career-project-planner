from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile


def extract_resume_text_from_file(file_bytes: bytes, filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension in {".txt", ".md"}:
        return decode_text_file(file_bytes)

    if extension == ".docx":
        return extract_docx_text(file_bytes)

    raise ValueError("Unsupported resume file type. Use .txt, .md, or .docx.")


def decode_text_file(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return file_bytes.decode("latin-1")


def extract_docx_text(file_bytes: bytes) -> str:
    try:
        with ZipFile(BytesIO(file_bytes)) as archive:
            document_xml = archive.read("word/document.xml")
    except (BadZipFile, KeyError) as exc:
        raise ValueError("Invalid .docx resume file.") from exc

    root = ElementTree.fromstring(document_xml)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    text_nodes = root.findall(".//w:t", namespace)

    return " ".join(node.text for node in text_nodes if node.text)
