from pathlib import Path
from typing import Dict, List

import fitz  # PyMuPDF


def list_papers(papers_dir: str) -> List[Path]:
    """
    Return all PDF files inside the configured papers directory.
    """

    directory = Path(papers_dir)

    if not directory.exists():
        raise FileNotFoundError(f"Papers directory not found: {papers_dir}")

    return sorted(directory.glob("*.pdf"))


def extract_pdf_text(pdf_path: str) -> Dict:
    """
    Extract text from a PDF page by page.

    Returns
    -------
    dict
        {
            "filename": ...,
            "path": ...,
            "page_count": ...,
            "pages": [
                {
                    "page_number": 1,
                    "text": "..."
                },
                ...
            ]
        }
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = fitz.open(path)

    pages = []

    for index, page in enumerate(document):
        text = page.get_text("text")

        pages.append(
            {
                "page_number": index + 1,
                "text": text.strip(),
            }
        )

    result = {
        "filename": path.name,
        "path": str(path),
        "page_count": len(document),
        "pages": pages,
    }

    document.close()

    return result


def load_all_papers(papers_dir: str) -> Dict[str, Dict]:
    """
    Load every PDF in the papers directory.

    The dictionary key is the PDF stem.

    Example:
        inputs/papers/LINGER.pdf
        becomes:
        papers["LINGER"]
    """

    papers = {}

    for pdf_path in list_papers(papers_dir):
        method_name = pdf_path.stem
        papers[method_name] = extract_pdf_text(str(pdf_path))

    return papers