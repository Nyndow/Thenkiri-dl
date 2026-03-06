import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from searcher.searcher.spiders.searching import SearchingSpider
from models import SearchResult

results = []

class CollectPipeline:
    def process_item(self, item, spider):
        results.append(item)
        return item

def main(query):
    settings = get_project_settings()
    settings.set("LOG_ENABLED", False)
    settings.set("ITEM_PIPELINES", {__name__ + ".CollectPipeline": 1})

    process = CrawlerProcess(settings)
    process.crawl(SearchingSpider, query=query)
    process.start()  

    for r in results:
        print(f"{r.title}|||{r.url}")

if __name__ == "__main__":
    query = sys.argv[1]
    main(query)