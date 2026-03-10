import scrapy
from models import Episode


class EpisodeSpider(scrapy.Spider):
    name = "episodes"

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        links = response.xpath(
            "//a[contains(., 'Download Episode') or contains(., 'Download Movie')]/@href"
        ).getall()

        for i, link in enumerate(links, 1):
            yield Episode(
                number=i,
                url=link
            )