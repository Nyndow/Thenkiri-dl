import scrapy


class DownloadSpider(scrapy.Spider):
    name = "download"

    def __init__(self, urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = urls.split(",") if urls else []

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):

        formdata = {
            "op": response.xpath("//input[@name='op']/@value").get(),
            "id": response.xpath("//input[@name='id']/@value").get(),
            "rand": response.xpath("//input[@name='rand']/@value").get(),
            "referer": response.xpath("//input[@name='referer']/@value").get(),
            "method_free": response.xpath("//input[@name='method_free']/@value").get(),
        }

        yield scrapy.FormRequest(
            url=response.url,
            formdata=formdata,
            callback=self.parse_final,
            meta={"episode_page": response.url}
        )

    def parse_final(self, response):

        download_url = response.xpath("//a[button[contains(@class,'downloadbtn')]]/@href").get()

        if download_url:
            yield {
                "episode_page": response.meta["episode_page"],
                "download_url": response.urljoin(download_url)
            }