from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_text_splitter(chunk_size=500, chunk_overlap=100):
    """
    Returns a configured RecursiveCharacterTextSplitter.
    Parameters are customizable for future tuning.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",  # paragraphs
            "\n",    # lines
            ".",     # sentences
            " ",     # words
            ""
        ]
    )


def split_text_with_metadata(text: str, source: str):
    """
    Splits text into chunks and attaches metadata.
    
    Args:
        text (str): Full document text
        source (str): Filename or document identifier

    Returns:
        List[Dict]: List of chunks with metadata
    """
    if not text or not text.strip():
        return []

    splitter = get_text_splitter()
    chunks = splitter.split_text(text)

    structured_chunks = []

    for i, chunk in enumerate(chunks):
        cleaned_chunk = chunk.strip()

        if not cleaned_chunk:
            continue  # skip empty chunks

        structured_chunks.append({
            "content": cleaned_chunk,
            "metadata": {
                "source": source,
                "chunk_id": i,
                "length": len(cleaned_chunk)  # useful for debugging/ranking
            }
        })

    return structured_chunks