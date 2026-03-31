   # document loading
import os
import pdfplumber
from docx import Document as DocxDocument
from src.processing.text_splitter import split_text_with_metadata


class DocumentLoader:

    def __init__(self, data_path="data/raw"):
        self.data_path = data_path

    def load_documents(self):
        """
        Loads and chunks all supported documents
        Supported formats: PDF, DOCX, TXT
        """
        all_chunks = []

        if not os.path.isdir(self.data_path):
            return all_chunks

        for file in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, file)

            if file.endswith(".pdf"):
                all_chunks.extend(self.load_pdf(file_path))

            elif file.endswith(".docx"):
                all_chunks.extend(self.load_docx(file_path))

            elif file.endswith(".txt"):
                all_chunks.extend(self.load_txt(file_path))

        return all_chunks

    def remove_reversed_words(self, text):
        words = text.split()
        cleaned = []
        for w in words:
            if len(w) > 6 and w[::-1].istitle():
                continue
            cleaned.append(w)

        return " ".join(cleaned)

    def load_pdf(self, file_path):
        all_chunks = []

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()

                if text:
                    text = self.remove_reversed_words(text)

                    chunks = split_text_with_metadata(
                        text,
                        source=os.path.basename(file_path)
                    )

                    # add page info to metadata
                    for chunk in chunks:
                        chunk["metadata"]["page"] = i + 1

                    all_chunks.extend(chunks)

        return all_chunks

    def load_docx(self, file_path):
        doc = DocxDocument(file_path)

        full_text = "\n".join([para.text for para in doc.paragraphs])

        chunks = split_text_with_metadata(
            full_text,
            source=os.path.basename(file_path)
        )

        return chunks

    def load_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = split_text_with_metadata(
            text,
            source=os.path.basename(file_path)
        )

        return chunks
