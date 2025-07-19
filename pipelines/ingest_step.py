"""
Ingestion Pipeline Step for OMNIMIND

Handles data ingestion using the basic loader.
"""

from typing import List, Dict, Any
import logging
from crawlers.basic_loader import BasicLoader

logger = logging.getLogger(__name__)


def ingest_step(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Ingest data from URLs or files."""
    try:
        sources = input_data.get("sources", [])
        if not sources:
            logger.warning("No sources provided for ingestion")
            return {"documents": [], "error": "No sources provided"}
        
        # Initialize loader
        loader = BasicLoader()
        
        # Load documents from sources
        documents = loader.load_multiple(sources)
        
        # Filter successful loads
        successful_docs = [doc for doc in documents if doc.get("success", False)]
        failed_docs = [doc for doc in documents if not doc.get("success", False)]
        
        # Log results
        logger.info(f"Ingested {len(successful_docs)} documents successfully")
        if failed_docs:
            logger.warning(f"Failed to ingest {len(failed_docs)} documents")
        
        # Clean up
        loader.close()
        
        return {
            "documents": successful_docs,
            "failed_documents": failed_docs,
            "total_sources": len(sources),
            "successful_ingestions": len(successful_docs),
            "failed_ingestions": len(failed_docs)
        }
        
    except Exception as e:
        logger.error(f"Error in ingest step: {e}")
        return {"error": str(e), "documents": []} 