"""
File Ingestor for OMNIMIND

Handles ingestion of files from local and remote sources.
"""

import os
import requests
from pathlib import Path
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


class FileIngestor:
    """File ingestor for processing various file formats."""
    
    SUPPORTED_FORMATS = ['.txt', '.md', '.pdf', '.docx', '.csv', '.json']
    
    def __init__(self, base_path: str = "./data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def ingest_local_file(self, file_path: str) -> Dict[str, Any]:
        """Ingest a local file and return its content."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if file_path.suffix not in self.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_size": file_path.stat().st_size,
                "content": content,
                "file_type": file_path.suffix
            }
        except Exception as e:
            logger.error(f"Error ingesting file {file_path}: {e}")
            return {"file_path": str(file_path), "error": str(e)}
    
    def ingest_remote_file(self, url: str, filename: str = None) -> Dict[str, Any]:
        """Download and ingest a remote file."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            if filename is None:
                filename = url.split('/')[-1]
            
            file_path = self.base_path / filename
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return self.ingest_local_file(str(file_path))
        except Exception as e:
            logger.error(f"Error ingesting remote file {url}: {e}")
            return {"url": url, "error": str(e)}
    
    def ingest_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Ingest all supported files from a directory."""
        results = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory_path}")
            return results
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.SUPPORTED_FORMATS:
                result = self.ingest_local_file(str(file_path))
                results.append(result)
        
        return results 