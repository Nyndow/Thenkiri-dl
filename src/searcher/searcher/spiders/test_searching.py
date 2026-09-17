import unittest

from scrapy.http import HtmlResponse

from searcher.searcher.spiders.searching import SearchingSpider
from models import SearchResult


PAGE_WITH_NEXT = """
<html><body>
<h2><a title="Show One" href="https://thenkiri.com/show-one/">Show One</a></h2>
<h2><a title="Show Two" href="https://thenkiri.com/show-two/">Show Two</a></h2>
<div class="oceanwp-pagination clr"><ul class="page-numbers">
  <li><span aria-current="page" class="page-numbers current">1</span></li>
  <li><a class="page-numbers" href="https://thenkiri.com/page/2/?s=love&post_type=post">2</a></li>
  <li><a class="next page-numbers" href="https://thenkiri.com/page/2/?s=love&post_type=post">Next</a></li>
</ul></div>
</body></html>
"""

PAGE_WITHOUT_NEXT = """
<html><body>
<h2><a title="Show Three" href="https://thenkiri.com/show-three/">Show Three</a></h2>
<div class="oceanwp-pagination clr"><ul class="page-numbers">
  <li><a class="page-numbers" href="https://thenkiri.com/page/1/?s=love&post_type=post">1</a></li>
  <li><span aria-current="page" class="page-numbers current">2</span></li>
</ul></div>
</body></html>
"""


def _response(url, body):
    return HtmlResponse(url=url, body=body.encode("utf-8"))


class SearchingSpiderUrlTests(unittest.TestCase):
    def test_page_one_uses_base_search_url(self):
        spider = SearchingSpider(query="love", site=0, page=1)
        self.assertEqual(
            spider.start_urls,
            ["https://thenkiri.com/?s=love&post_type=post"],
        )

    def test_page_two_uses_wordpress_page_path(self):
        spider = SearchingSpider(query="love", site=0, page=2)
        self.assertEqual(
            spider.start_urls,
            ["https://thenkiri.com/page/2/?s=love&post_type=post"],
        )

    def test_dramakey_site_uses_its_own_domain(self):
        spider = SearchingSpider(query="love", site=1, page=3)
        self.assertEqual(
            spider.start_urls,
            ["https://dramakey.com/page/3/?s=love&post_type=post"],
        )

    def test_empty_query_raises(self):
        with self.assertRaises(ValueError):
            SearchingSpider(query=None, site=0, page=1)

    def test_invalid_site_raises(self):
        with self.assertRaises(ValueError):
            SearchingSpider(query="love", site=2, page=1)


class SearchingSpiderParseTests(unittest.TestCase):
    def test_yields_a_result_per_show(self):
        spider = SearchingSpider(query="love", site=0, page=1)
        response = _response("https://thenkiri.com/?s=love&post_type=post", PAGE_WITH_NEXT)

        results = list(spider.parse(response))

        self.assertEqual(
            results,
            [
                SearchResult(title="Show One", url="https://thenkiri.com/show-one/"),
                SearchResult(title="Show Two", url="https://thenkiri.com/show-two/"),
            ],
        )

    def test_sets_has_next_true_when_next_link_present(self):
        spider = SearchingSpider(query="love", site=0, page=1)
        response = _response("https://thenkiri.com/?s=love&post_type=post", PAGE_WITH_NEXT)

        list(spider.parse(response))

        self.assertTrue(spider.has_next)

    def test_sets_has_next_false_on_last_page(self):
        spider = SearchingSpider(query="love", site=0, page=2)
        response = _response("https://thenkiri.com/page/2/?s=love&post_type=post", PAGE_WITHOUT_NEXT)

        list(spider.parse(response))

        self.assertFalse(spider.has_next)


if __name__ == "__main__":
    unittest.main()
