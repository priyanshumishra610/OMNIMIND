"""
Web Crawler for OMNIMIND

Handles web scraping and data extraction from various sources.
"""

import scrapy
from newspaper import Article
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class WebCrawler:
    """Web crawler for extracting content from web pages."""
    
    def __init__(self, allowed_domains: List[str] = None):
        self.allowed_domains = allowed_domains or []
        self.extracted_data = []
    
    def crawl_url(self, url: str) -> Dict[str, Any]:
        """Extract content from a single URL."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            return {
                "url": url,
                "title": article.title,
                "text": article.text,
                "summary": article.summary,
                "keywords": article.keywords,
                "publish_date": article.publish_date,
                "authors": article.authors
            }
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return {"url": url, "error": str(e)}
    
    def crawl_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Crawl multiple URLs and return extracted data."""
        results = []
        for url in urls:
            result = self.crawl_url(url)
            results.append(result)
        return results


class OMNIMINDSpider(scrapy.Spider):
    """Scrapy spider for OMNIMIND web crawling."""
    
    name = "omnimind_spider"
    
    def __init__(self, start_urls=None, *args, **kwargs):
        super(OMNIMINDSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls or []
    
    def parse(self, response):
        """Parse the response and extract content."""
        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "content": response.css("body::text").get(),
            "links": response.css("a::attr(href)").getall()
        } 