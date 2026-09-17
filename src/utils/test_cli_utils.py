import unittest
from unittest.mock import patch, MagicMock

from utils.cli_utils import choose_from_search


def _ask_sequence(*answers):
    mocks = []
    for answer in answers:
        m = MagicMock()
        m.ask.return_value = answer
        mocks.append(m)
    return mocks


class ChooseFromSearchPaginationTests(unittest.TestCase):
    def setUp(self):
        clear_patcher = patch("utils.cli_utils.clear")
        input_patcher = patch("builtins.input", return_value="some query")
        self.mock_clear = clear_patcher.start()
        self.mock_input = input_patcher.start()
        self.addCleanup(clear_patcher.stop)
        self.addCleanup(input_patcher.stop)

    @patch("utils.cli_utils.run_searching")
    @patch("questionary.select")
    def test_next_page_fetches_page_two_and_selecting_returns_it(self, mock_select, mock_run_searching):
        mock_select.side_effect = _ask_sequence(
            "0",              # site menu
            "__next_page__",  # page 1 -> go to page 2
            "Show B",         # pick a page-2 result
        )
        mock_run_searching.side_effect = [
            ([{"title": "Show A", "url": "url-a"}], True),
            ([{"title": "Show B", "url": "url-b"}], False),
        ]

        result = choose_from_search()

        self.assertEqual(result, {"title": "Show B", "url": "url-b"})
        self.assertEqual(mock_run_searching.call_count, 2)
        mock_run_searching.assert_any_call("some query", "0", 1)
        mock_run_searching.assert_any_call("some query", "0", 2)

    @patch("utils.cli_utils.run_searching")
    @patch("questionary.select")
    def test_previous_page_reuses_cached_results(self, mock_select, mock_run_searching):
        mock_select.side_effect = _ask_sequence(
            "0",
            "__next_page__",  # page 1 -> page 2
            "__prev_page__",  # page 2 -> back to page 1
            "Show A",         # pick the cached page-1 result
        )
        mock_run_searching.side_effect = [
            ([{"title": "Show A", "url": "url-a"}], True),
            ([{"title": "Show B", "url": "url-b"}], False),
        ]

        result = choose_from_search()

        self.assertEqual(result, {"title": "Show A", "url": "url-a"})
        self.assertEqual(mock_run_searching.call_count, 2)

    @patch("utils.cli_utils.run_searching")
    @patch("questionary.select")
    def test_no_results_returns_none(self, mock_select, mock_run_searching):
        mock_select.side_effect = _ask_sequence("0")
        mock_run_searching.return_value = ([], False)

        result = choose_from_search()

        self.assertIsNone(result)

    @patch("utils.cli_utils.run_searching")
    @patch("questionary.select")
    def test_cancelling_selection_returns_none(self, mock_select, mock_run_searching):
        mock_select.side_effect = _ask_sequence("0", None)
        mock_run_searching.return_value = ([{"title": "Show A", "url": "url-a"}], False)

        result = choose_from_search()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
