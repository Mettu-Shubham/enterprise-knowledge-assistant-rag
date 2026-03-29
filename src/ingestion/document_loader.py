#document loading 
import os
import pdfplumber
from docx import Document as DocxDocument
from langchain.schema import Document


class DocumentLoader:

    def __init__(self, data_path="data/raw"):
        self.data_path = data_path

    def load_documents(self):
        """
        Loads all supported documents from data/raw
        Supported formats: PDF, DOCX, TXT
        """
        documents = []

        for file in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, file)

            if file.endswith(".pdf"):
                documents.extend(self.load_pdf(file_path))

            elif file.endswith(".docx"):
                documents.extend(self.load_docx(file_path))

            elif file.endswith(".txt"):
                documents.extend(self.load_txt(file_path))

        return documents

    def remove_reversed_words(self, text):
        words = text.split()
        cleaned = []
        for w in words:
            if len(w) > 6 and w[::-1].istitle():
                continue
            cleaned.append(w)

        return " ".join(cleaned)

    def load_pdf(self, file_path):
        docs = []

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()

                if text:
                    text =self.remove_reversed_words(text)
                    docs.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": file_path,
                                "page": i + 1
                            }
                        )
                    )

        return docs

    def load_docx(self, file_path):
        docs = []
        doc = DocxDocument(file_path)

        full_text = "\n".join([para.text for para in doc.paragraphs])

        docs.append(
            Document(
                page_content=full_text,
                metadata={"source": file_path}
            )
        )

        return docs

    def load_txt(self, file_path):
        docs = []

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        docs.append(
            Document(
                page_content=text,
                metadata={"source": file_path}
            )
        )

        return docs