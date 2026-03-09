import scrapy
from urllib.parse import quote_plus
from models import SearchResult

class SearchingSpider(scrapy.Spider):
    name = "searching"

    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not query:
            raise ValueError("Query cannot be empty")

        self.start_urls = [
            f"https://thenkiri.com/?s={quote_plus(query)}&post_type=post"
        ]

    def parse(self, response):
        for h2 in response.css("h2"):
            a_tag = h2.css("a")

            if a_tag:
                title = a_tag.attrib.get("title") or a_tag.css("::text").get()
                url = a_tag.attrib.get("href")

                if url:
                    yield SearchResult(title=title, url=url)