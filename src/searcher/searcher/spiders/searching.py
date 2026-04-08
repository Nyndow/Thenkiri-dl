import scrapy
from urllib.parse import quote_plus
from models import SearchResult

class SearchingSpider(scrapy.Spider):
    name = "searching"

    def __init__(self, query=None, site=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not query:
            raise ValueError("Query cannot be empty")

        site = int(site)
        if site == 0:
            self.start_urls = [f"https://thenkiri.com/?s={quote_plus(query)}&post_type=post"]
        elif site == 1:
            self.start_urls = [f"https://dramakey.com/?s={quote_plus(query)}&post_type=post"]
        else:
            raise ValueError("Invalid site: use 0 for thenkiri.com or 1 for dramakey.com")

    def parse(self, response):
        for h2 in response.css("h2"):
            a_tag = h2.css("a")
            if a_tag:
                title = a_tag.attrib.get("title") or a_tag.css("::text").get()
                url = a_tag.attrib.get("href")
                if url:
                    yield SearchResult(title=title, url=url)
