import scrapy
from models import SearchResult

class SearchingSpider(scrapy.Spider):
    name = "searching"

    def __init__(self, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://thenkiri.com/?s={query}&post_type=post"]

    def parse(self, response):
        for h2 in response.css("h2"):
            a_tag = h2.css("a")

            if a_tag:
                result = SearchResult(
                    title=a_tag.attrib.get("title"),
                    url=a_tag.attrib.get("href")
                )

                yield result