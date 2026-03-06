import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from searcher.searcher.spiders.download import DownloadSpider

downloads = []

class DownloadPipeline:
    def process_item(self, item, spider):
        downloads.append(item)
        return item


def main(urls):
    settings = get_project_settings()
    settings.set("LOG_ENABLED", False)
    settings.set("ITEM_PIPELINES", {__name__ + ".DownloadPipeline": 1})

    process = CrawlerProcess(settings)
    process.crawl(DownloadSpider, urls=urls)
    process.start()

    for item in downloads:
        print(f"{item['episode_page']}|||{item['download_url']}")


if __name__ == "__main__":
    urls = sys.argv[1]
    main(urls)