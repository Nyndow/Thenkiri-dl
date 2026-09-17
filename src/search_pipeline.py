import sys
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from searcher.searcher.spiders.searching import SearchingSpider

results = []
pagination = {"has_next": False}

class CollectPipeline:
    def process_item(self, item, spider):
        results.append(item)
        return item

def _record_pagination(spider):
    pagination["has_next"] = getattr(spider, "has_next", False)

def main(query, site=0, page=1):
    settings = get_project_settings()
    settings.set("LOG_ENABLED", True)
    settings.set("ITEM_PIPELINES", {__name__ + ".CollectPipeline": 1})
    process = CrawlerProcess(settings)
    crawler = process.create_crawler(SearchingSpider)
    crawler.signals.connect(_record_pagination, signal=signals.spider_closed)
    process.crawl(crawler, query=query, site=site, page=page)
    process.start()
    for r in results:
        print(f"RESULT|||{r.title}|||{r.url}")
    print(f"HASNEXT|||{'true' if pagination['has_next'] else 'false'}")

if __name__ == "__main__":
    query = sys.argv[1]
    site = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    page = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    main(query, site, page)
