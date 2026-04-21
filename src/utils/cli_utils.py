import os
import logging
import questionary

from utils.pipeline_utils import run_searching, run_episode, run_download
from utils.download_utils import download_with_aria2, download_with_wget
from utils.settings_utils import settings_cli

LOG_PATH = os.path.expanduser(os.getenv("THENKIRI_LOG_PATH", "./logs/thenkiri.log"))
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.FileHandler(LOG_PATH)]
)

logger = logging.getLogger(__name__)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def choose_from_search():
    try:
        while True:
            clear()

            site = questionary.select(
                "What do you want to do?",
                choices=[
                    questionary.Choice(title="Korean dramas & movies", value="0"),
                    questionary.Choice(title="Chinese dramas (dramakey.com)", value="1"),
                    questionary.Choice(title="Settings", value="settings"),
                    questionary.Choice(title="Exit", value="exit"),
                ]
            ).ask()

            if not site:
                return None

            if site == "exit":
                return None

            if site == "settings":
                settings_cli()
                continue

            query = input("Search for a show: ")
            search_results = run_searching(query, site)

            if not search_results:
                print("No results found.")
                input("\nPress Enter...")
                continue

            print("\nResults:\n")

            choices = [r["title"] for r in search_results]

            selected_title = questionary.select(
                "Choose result:",
                choices=choices
            ).ask()

            if not selected_title:
                return None

            selected = next(r for r in search_results if r["title"] == selected_title)

            print(f"\nSelected: {selected['title']}")
            print(selected["url"])

            return selected

    except Exception:
        logger.exception("Error during search")
        return None


def choose_episodes(selected):
    if not selected:
        return [], None

    try:
        episode_list = run_episode(selected["url"])

        if not episode_list:
            print("No episodes found.")
            return [], None

        print(f"\nEpisodes for {selected['title']}:\n")

        # single episode
        if len(episode_list) == 1:
            ep = episode_list[0]
            print(f"Only one episode: {ep['number']}")

            confirm = questionary.confirm("Download this episode?").ask()
            if not confirm:
                return [], None

            episode_urls = ep["url"]

        # multiple episodes
        else:
            choices = [
                questionary.Choice(title="Select All", value="__all__")
            ] + [
                questionary.Choice(
                    title=f"Episode {ep['number']}",
                    value=ep["url"]
                )
                for ep in episode_list
            ]

            selected_episode_urls = questionary.checkbox(
                "Select episodes (SPACE to select):",
                choices=choices
            ).ask()

            if not selected_episode_urls:
                return [], None

            if "__all__" in selected_episode_urls:
                episode_urls = ",".join(ep["url"] for ep in episode_list)
            else:
                episode_urls = ",".join(selected_episode_urls)

        downloads = run_download(episode_urls)

        if not downloads:
            return [], None

        # 🔥 return folder name too
        return downloads, selected["title"]

    except Exception:
        logger.exception("Error selecting episodes")
        return [], None


def choose_downloader_and_start(downloads, folder_name):
    if not downloads:
        print("No downloads.")
        return

    def sanitize(name: str) -> str:
        import re
        return re.sub(r'[\\/*?:"<>|]', "", name or "default")

    folder_name = sanitize(folder_name)

    try:
        downloader = questionary.select(
            "Choose downloader:",
            choices=[
                "aria2 (fast multi-connection)",
                "wget (simple downloader)"
            ]
        ).ask()

        if not downloader:
            return

        for d in downloads:
            url = d.get("download_url")
            if not url:
                continue

            print(f"Downloading: {url}")

            try:
                if downloader.startswith("aria2"):
                    download_with_aria2(url, folder_name)
                else:
                    download_with_wget(url, folder_name)

            except Exception:
                logger.exception("Download failed: %s", url)

    except Exception:
        logger.exception("Downloader error")


def run_cli():
    try:
        selected = choose_from_search()
        downloads, folder_name = choose_episodes(selected)
        choose_downloader_and_start(downloads, folder_name)

    except Exception:
        logger.exception("Unexpected CLI error")