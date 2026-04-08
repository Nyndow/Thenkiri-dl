import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from searcher.searcher.spiders.searching import SearchingSpider

results = []

class CollectPipeline:
    def process_item(self, item, spider):
        results.append(item)
        return item

def main(query, site=0):
    settings = get_project_settings()
    settings.set("LOG_ENABLED", True)
    settings.set("ITEM_PIPELINES", {__name__ + ".CollectPipeline": 1})
    process = CrawlerProcess(settings)
    process.crawl(SearchingSpider, query=query, site=site)
    process.start()
    for r in results:
        print(f"{r.title}|||{r.url}")

if __name__ == "__main__":
    query = sys.argv[1]
    site = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    main(query, site)
