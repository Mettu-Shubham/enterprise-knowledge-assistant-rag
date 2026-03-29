# make chunks from docs
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(
        self,
        chunk_size=800,
        chunk_overlap=150
    ):
        """
        chunk_size: max characters per chunk
        chunk_overlap: overlap between chunks
        """

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,

            # Important separators for structured splitting
            separators=[
                "\n\n",   # paragraphs
                "\n",     # new lines
                ".",      # sentences
                " ",
                ""
            ]
        )

    def split_documents(self, documents):
        """
        Convert documents into chunks
        """

        chunks = self.splitter.split_documents(documents)

        return chunks