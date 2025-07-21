import random 
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter


def generate_chunks_from_pdf(pdf_path): 
    pdf_txt_extracted = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pdf_txt_extracted += text + "\n"

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.create_documents([pdf_txt_extracted])
    return chunks
  
def generate_simulated_progress():
    numbers = [random.randint(start, start + 9) for start in range(1, 100, 10)]
    return numbers