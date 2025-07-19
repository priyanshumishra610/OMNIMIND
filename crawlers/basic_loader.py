"""
Basic Loader for OMNIMIND

Handles loading data from URLs and local files, outputting raw text.
"""

import os
import requests
from pathlib import Path
from typing import List, Dict, Any, Union
import logging
from urllib.parse import urlparse
import time

logger = logging.getLogger(__name__)


class BasicLoader:
    """Basic data loader for URLs and local files."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OMNIMIND/1.0 (https://github.com/priyanshumishra610/omnimind)'
        })
    
    def load_url(self, url: str) -> Dict[str, Any]:
        """Load content from a URL."""
        try:
            for attempt in range(self.max_retries):
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    response.raise_for_status()
                    
                    # Extract text content
                    content = self._extract_text_from_response(response)
                    
                    return {
                        "source": url,
                        "content": content,
                        "content_type": response.headers.get('content-type', ''),
                        "status_code": response.status_code,
                        "size_bytes": len(response.content),
                        "success": True
                    }
                    
                except requests.RequestException as e:
                    if attempt == self.max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
        except Exception as e:
            logger.error(f"Failed to load URL {url}: {e}")
            return {
                "source": url,
                "content": "",
                "error": str(e),
                "success": False
            }
    
    def load_file(self, file_path: str) -> Dict[str, Any]:
        """Load content from a local file."""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Check file size (limit to 10MB)
            file_size = file_path.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB
                raise ValueError(f"File too large: {file_size} bytes")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "source": str(file_path),
                "content": content,
                "content_type": "text/plain",
                "size_bytes": file_size,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Failed to load file {file_path}: {e}")
            return {
                "source": str(file_path),
                "content": "",
                "error": str(e),
                "success": False
            }
    
    def load_multiple(self, sources: List[str]) -> List[Dict[str, Any]]:
        """Load content from multiple sources (URLs or files)."""
        results = []
        
        for source in sources:
            if self._is_url(source):
                result = self.load_url(source)
            else:
                result = self.load_file(source)
            results.append(result)
        
        return results
    
    def _is_url(self, source: str) -> bool:
        """Check if source is a URL."""
        try:
            result = urlparse(source)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _extract_text_from_response(self, response: requests.Response) -> str:
        """Extract text content from HTTP response."""
        content_type = response.headers.get('content-type', '').lower()
        
        if 'text/html' in content_type:
            # Basic HTML text extraction
            from bs4 import BeautifulSoup
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                return soup.get_text(separator=' ', strip=True)
            except ImportError:
                logger.warning("BeautifulSoup not available, returning raw HTML")
                return response.text
        elif 'text/plain' in content_type or 'application/json' in content_type:
            return response.text
        else:
            # Try to decode as text anyway
            try:
                return response.text
            except:
                return str(response.content)
    
    def close(self):
        """Close the session."""
        self.session.close() 