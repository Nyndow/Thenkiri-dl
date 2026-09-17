import scrapy
from urllib.parse import quote_plus
from models import SearchResult

class SearchingSpider(scrapy.Spider):
    name = "searching"

    SITES = {
        0: "https://thenkiri.com",
        1: "https://dramakey.com",
    }

    def __init__(self, query=None, site=0, page=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not query:
            raise ValueError("Query cannot be empty")

        site = int(site)
        if site not in self.SITES:
            raise ValueError("Invalid site: use 0 for thenkiri.com or 1 for dramakey.com")

        page = int(page)
        base_url = self.SITES[site]
        search_qs = f"s={quote_plus(query)}&post_type=post"

        if page > 1:
            self.start_urls = [f"{base_url}/page/{page}/?{search_qs}"]
        else:
            self.start_urls = [f"{base_url}/?{search_qs}"]

        self.has_next = False

    def parse(self, response):
        for h2 in response.css("h2"):
            a_tag = h2.css("a")
            if a_tag:
                title = a_tag.attrib.get("title") or a_tag.css("::text").get()
                url = a_tag.attrib.get("href")
                if url:
                    yield SearchResult(title=title, url=url)

        self.has_next = bool(response.css("a.next.page-numbers::attr(href)").get())
