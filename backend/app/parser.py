import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")
    return text

def clean_resume_text(text: str) -> str:
    """
    Cleans extracted text using basic string techniques.
    """
    # Simply remove excess newlines and spaces
    clean_text = " ".join(text.split())
    return clean_text

def parse_resume(pdf_path: str) -> str:
    """
    Main pipeline to get cleaned text from PDF.
    """
    raw_text = extract_text_from_pdf(pdf_path)
    return clean_resume_text(raw_text)
