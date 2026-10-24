from typing import List, Union, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..utils.logger import logger

def get_text_splitter(chunk_size: int = 600, chunk_overlap: int = 100) -> RecursiveCharacterTextSplitter:
    """
    Returns an optimized LangChain RecursiveCharacterTextSplitter for banking policy text.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )

def split_text_into_chunks(
    documents: List[Union[Document, Dict[str, Any]]],
    chunk_size: int = 600,
    chunk_overlap: int = 100
) -> List[Document]:
    """
    LangChain Pipeline: Splits documents into semantically coherent chunks using
    RecursiveCharacterTextSplitter while maintaining full source provenance metadata.
    """
    splitter = get_text_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    langchain_docs: List[Document] = []

    for d in documents:
        if isinstance(d, Document):
            langchain_docs.append(d)
        elif isinstance(d, dict):
            langchain_docs.append(Document(
                page_content=d.get("text", d.get("page_content", "")),
                metadata={"source": d.get("source", "unknown"), "file_path": d.get("file_path", "")}
            ))

    chunks = splitter.split_documents(langchain_docs)

    # Attach unique chunk ids
    for idx, c in enumerate(chunks):
        c.metadata["chunk_id"] = f"chunk-{idx}"

    logger.info(f"[LangChain Splitter] Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks
