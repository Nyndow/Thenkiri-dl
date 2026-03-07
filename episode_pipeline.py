import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from searcher.searcher.spiders.episodes import EpisodeSpider

episodes = []

class EpisodePipeline:
    def process_item(self, item, spider):
        episodes.append(item)
        return item

def main(url):
    settings = get_project_settings()
    settings.set("LOG_ENABLED", False)
    settings.set("ITEM_PIPELINES", {__name__ + ".EpisodePipeline": 1})

    process = CrawlerProcess(settings)
    process.crawl(EpisodeSpider, url=url)
    process.start()

    for ep in episodes:
        print(f"{ep.number}|||{ep.url}")

if __name__ == "__main__":
    url = sys.argv[1]
    main(url)