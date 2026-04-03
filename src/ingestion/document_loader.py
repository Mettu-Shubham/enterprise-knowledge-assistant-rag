import os
import pdfplumber
from docx import Document as DocxDocument

from src.ingestion.document_registry import DocumentRegistry
from src.processing.text_splitter import split_text_with_metadata


class DocumentLoader:

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

    def __init__(self, data_path="data/WorldBank", registry_path="data/document_registry.json"):
        self.data_path = data_path
        self.registry = DocumentRegistry(registry_path)

    def load_documents(self, changed_only=False):
        """
        Recursively load and chunk supported documents from nested folders.

        If changed_only=True:
        - process only new and modified files
        - skip unchanged files
        - still track deleted files in registry
        """
        all_chunks = []

        if not os.path.isdir(self.data_path):
            return {
                "chunks": [],
                "changes": {
                    "new": [],
                    "modified": [],
                    "deleted": [],
                    "unchanged": [],
                },
                "documents": [],
            }

        previous_registry = self.registry.load()
        previous_documents = previous_registry.get("documents", [])

        current_documents = []
        for file_path in self.discover_files():
            registry_entry = self.registry.build_entry(file_path, self.data_path)
            current_documents.append(registry_entry)

        changes = self.registry.detect_changes(previous_documents, current_documents)

        if changed_only:
            allowed_paths = set(changes["new"] + changes["modified"])
        else:
            allowed_paths = {doc["relative_path"] for doc in current_documents}

        for registry_entry in current_documents:
            if registry_entry["relative_path"] not in allowed_paths:
                continue

            file_path = registry_entry["absolute_path"]
            extension = os.path.splitext(file_path)[1].lower()

            if extension == ".pdf":
                chunks = self.load_pdf(file_path, registry_entry)
            elif extension == ".docx":
                chunks = self.load_docx(file_path, registry_entry)
            elif extension == ".txt":
                chunks = self.load_txt(file_path, registry_entry)
            else:
                continue

            all_chunks.extend(chunks)

        self.registry.save(current_documents, changes=changes)

        return {
            "chunks": all_chunks,
            "changes": changes,
            "documents": current_documents,
        }

    def discover_files(self):
        discovered = []

        for root, _, files in os.walk(self.data_path):
            for file_name in files:
                extension = os.path.splitext(file_name)[1].lower()
                if extension in self.SUPPORTED_EXTENSIONS:
                    discovered.append(os.path.join(root, file_name))

        discovered.sort()
        return discovered

    def remove_reversed_words(self, text):
        words = text.split()
        cleaned = []

        for word in words:
            if len(word) > 6 and word[::-1].istitle():
                continue
            cleaned.append(word)

        return " ".join(cleaned)

    def load_pdf(self, file_path, registry_entry):
        all_chunks = []

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()

                if not text:
                    continue

                text = self.remove_reversed_words(text)
                chunks = split_text_with_metadata(
                    text,
                    source=registry_entry["source"]
                )

                for chunk in chunks:
                    chunk["metadata"].update({
                        "domain": registry_entry["domain"],
                        "classification": registry_entry["classification"],
                        "relative_path": registry_entry["relative_path"],
                        "file_type": registry_entry["file_type"],
                        "page": i + 1,
                    })

                all_chunks.extend(chunks)

        return all_chunks

    def load_docx(self, file_path, registry_entry):
        doc = DocxDocument(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])

        chunks = split_text_with_metadata(
            full_text,
            source=registry_entry["source"]
        )

        for chunk in chunks:
            chunk["metadata"].update({
                "domain": registry_entry["domain"],
                "classification": registry_entry["classification"],
                "relative_path": registry_entry["relative_path"],
                "file_type": registry_entry["file_type"],
            })

        return chunks

    def load_txt(self, file_path, registry_entry):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = split_text_with_metadata(
            text,
            source=registry_entry["source"]
        )

        for chunk in chunks:
            chunk["metadata"].update({
                "domain": registry_entry["domain"],
                "classification": registry_entry["classification"],
                "relative_path": registry_entry["relative_path"],
                "file_type": registry_entry["file_type"],
            })

        return chunks