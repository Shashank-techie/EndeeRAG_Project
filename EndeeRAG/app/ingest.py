import os
from typing import List
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".md"]


def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def load_documents(folder_path: str = "data/docs") -> List[str]:
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext not in SUPPORTED_EXTENSIONS:
            continue

        if ext == ".txt" or ext == ".md":
            text = read_txt(file_path)
        elif ext == ".pdf":
            text = read_pdf(file_path)
        else:
            continue

        if text.strip():
            documents.append(text)

    return documents


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Splits text into overlapping chunks for better semantic retrieval.
    """
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def prepare_chunks(folder_path: str = "data/docs") -> List[str]:
    docs = load_documents(folder_path)
    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)

    return all_chunks


if __name__ == "__main__":
    chunks = prepare_chunks()
    print(f"Loaded {len(chunks)} chunks from documents.")
