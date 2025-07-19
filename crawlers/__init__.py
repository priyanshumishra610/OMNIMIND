"""
OMNIMIND Crawlers Module

This module handles data ingestion from various sources:
- Web scraping with Scrapy
- File ingestion from local/remote sources
- RSS feeds and news aggregation
"""

from .web_crawler import WebCrawler
from .file_ingestor import FileIngestor
from .basic_loader import BasicLoader

__all__ = ["WebCrawler", "FileIngestor", "BasicLoader"] 