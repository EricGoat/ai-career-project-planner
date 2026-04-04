import io
from zipfile import ZipFile

import pytest

from backend.services.resume_file_parser import extract_resume_text_from_file


def test_extract_resume_text_from_text_file():
    result = extract_resume_text_from_file(
        b"Python SQL machine learning",
        "resume.txt"
    )

    assert result == "Python SQL machine learning"


def test_extract_resume_text_from_docx_file():
    file_buffer = io.BytesIO()

    with ZipFile(file_buffer, "w") as archive:
        archive.writestr(
            "word/document.xml",
            (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                "<w:body><w:p><w:r><w:t>Python</w:t></w:r></w:p>"
                "<w:p><w:r><w:t>SQL</w:t></w:r></w:p></w:body></w:document>"
            )
        )

    result = extract_resume_text_from_file(file_buffer.getvalue(), "resume.docx")

    assert result == "Python SQL"


def test_extract_resume_text_rejects_unsupported_file_types():
    with pytest.raises(ValueError, match="Unsupported resume file type"):
        extract_resume_text_from_file(b"fake-pdf", "resume.pdf")
