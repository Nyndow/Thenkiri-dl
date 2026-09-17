import unittest

from utils.pipeline_utils import _parse_search_output


class ParseSearchOutputTests(unittest.TestCase):
    def test_parses_result_lines_into_dicts(self):
        lines = [
            "RESULT|||Show One|||https://thenkiri.com/show-one/",
            "RESULT|||Show Two|||https://thenkiri.com/show-two/",
            "HASNEXT|||true",
        ]

        results, has_next = _parse_search_output(lines)

        self.assertEqual(
            results,
            [
                {"title": "Show One", "url": "https://thenkiri.com/show-one/"},
                {"title": "Show Two", "url": "https://thenkiri.com/show-two/"},
            ],
        )

    def test_has_next_true_when_flagged(self):
        lines = ["RESULT|||Show One|||https://thenkiri.com/show-one/", "HASNEXT|||true"]

        _, has_next = _parse_search_output(lines)

        self.assertTrue(has_next)

    def test_has_next_false_on_last_page(self):
        lines = ["RESULT|||Show One|||https://thenkiri.com/show-one/", "HASNEXT|||false"]

        _, has_next = _parse_search_output(lines)

        self.assertFalse(has_next)

    def test_no_results_returns_empty_list(self):
        results, has_next = _parse_search_output(["HASNEXT|||false"])

        self.assertEqual(results, [])
        self.assertFalse(has_next)


if __name__ == "__main__":
    unittest.main()
