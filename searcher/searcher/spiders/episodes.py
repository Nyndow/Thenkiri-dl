import scrapy
from models import Episode


class EpisodeSpider(scrapy.Spider):
    name = "episodes"

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        episode_links = response.xpath(
            "//a[contains(., 'Download Episode')]/@href"
        ).getall()

        for i, link in enumerate(episode_links, 1):
            yield Episode(
                number=i,
                url=link
            )