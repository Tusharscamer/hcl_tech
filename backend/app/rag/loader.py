from pathlib import Path
from typing import List
import pypdf
from langchain_core.documents import Document
from ..config.settings import settings
from ..utils.logger import logger

def load_policy_documents() -> List[Document]:
    """
    LangChain Document Loader: Extracts text from all banking policy PDFs
    in data/policies/ and returns standardized LangChain Document objects.
    """
    policies_dir = settings.POLICIES_DIR
    documents: List[Document] = []

    if not policies_dir.exists():
        logger.warning(f"[LangChain Loader] Policies directory not found: {policies_dir}")
        return documents

    for pdf_file in sorted(policies_dir.glob("*.pdf")):
        try:
            reader = pypdf.PdfReader(str(pdf_file))
            full_text = ""
            for idx, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                full_text += f"\n[Page {idx+1}]\n" + txt

            clean_text = full_text.strip()
            doc = Document(
                page_content=clean_text,
                metadata={
                    "source": pdf_file.name,
                    "file_path": str(pdf_file),
                    "total_pages": len(reader.pages)
                }
            )
            documents.append(doc)
            logger.info(f"[LangChain Loader] Loaded policy PDF: {pdf_file.name} ({len(clean_text)} chars)")
        except Exception as e:
            logger.error(f"[LangChain Loader] Error reading {pdf_file.name}: {e}")

    return documents
