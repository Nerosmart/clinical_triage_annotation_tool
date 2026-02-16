import os
from pathlib import Path

# Optional imports (activate when ready)

try:
    import docx # python-docx

except ImportError:
    docx = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

def extract_text(file_path: str) -> str:
    """
    Extract text from  .txt, .docx, or .pdf files.
    returns extracted text as a string.
    """

    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    # Check if file exists

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Route to the appropriate extraction function based on file extension
    
    if ext == ".txt":
        return _extract_txt(file_path)
    
    elif ext == ".docx":
        if docx is None:
            raise ImportError("Python-docx is not installed. Run: pip install python-docx")
        return _extract_docx(file_path)
    
    elif ext == ".pdf":
        if pdfplumber is None:
            raise ImportError("pdfplumber is not installed. Run: pip install pdfplumber")
        return _extract_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
def _extract_txt(path: Path) -> str:
    """
    Extract text from a plain .txt file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def extract_docx(Path) -> str:
    """
    Extract text from a .docx file using python-docx.
    """
    doc = docx.Document(Path)
    # Join all paragraphs with line breaks to preserve structure

    return "\n".join([para.text for para in doc.paragraphs])

def extract_pdf(Path) -> str:
    """
    Extract text from a .pdf file using pdfplumber.
    """
    text = []
    with pdfplumber.open(Path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            # Some pages may return None if empty or image-based.
            
            if page_text:
                text.append(page_text)
    return "\n".join(text)