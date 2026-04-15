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
                print("No selection made.")
                return None
            
            if site == "exit":
                return None

            if site == "settings":
                settings_cli()
                continue

            query = input("Search for a show: ")
            search_results = run_searching(query, site)

            if search_results is None:
                print("Search failed. Check logs for details.")
                input("\nPress Enter to continue...")
                continue

            if not search_results:
                print(f"No results found for: {query}")
                input("\nPress Enter to continue...")
                continue

            print("\nResults:\n")
            choices = [r["title"] for r in search_results]

            selected_title = questionary.select(
                "Choose result:",
                choices=choices
            ).ask()

            if not selected_title:
                print("No selection made.")
                input("\nPress Enter to continue...")
                continue

            selected = next(r for r in search_results if r["title"] == selected_title)

            print(f"\nSelected: {selected['title']}")
            print(selected["url"])

            return selected
    except Exception:
        logger.exception("Error during search")
        return None

def choose_episodes(selected):
    if not selected:
        return []

    try:
        episode_list = run_episode(selected["url"])

        if episode_list is None:
            print("Episode lookup failed. Check logs for details.")
            return []

        if not episode_list:
            print(f"No episodes found for {selected['title']}")
            return []

        print(f"\nEpisodes for {selected['url']}:\n")

        if len(episode_list) == 1:
            ep = episode_list[0]
            print(f"Only one episode found: Episode {ep['number']}")
            confirm = questionary.confirm("Download this episode?").ask()
            if not confirm:
                return []
            episode_urls = ep["url"]

        else:
            choices = [
                questionary.Choice(title="Select All", value="__all__")
            ] + [
                questionary.Choice(title=f"Episode {ep['number']}", value=ep["url"])
                for ep in episode_list
            ]

            selected_episode_urls = questionary.checkbox(
                "Select episodes (SPACE to select):",
                choices=choices
            ).ask()

            if not selected_episode_urls:
                print("No episodes selected.")
                return []

            if "__all__" in selected_episode_urls:
                episode_urls = ",".join(ep["url"] for ep in episode_list)
            else:
                episode_urls = ",".join(selected_episode_urls)

        downloads = run_download(episode_urls)

        if downloads is None:
            print("Download lookup failed. Check logs for details.")
            return []

        return downloads

    except Exception:
        logger.exception("Error while selecting episodes")
        return []

def choose_downloader_and_start(downloads):
    if not downloads:
        print("No downloads to process.")
        return

    try:
        downloader = questionary.select(
            "Choose downloader:",
            choices=[
                "aria2 (fast multi-connection)",
                "wget (simple downloader)"
            ]
        ).ask()

        if not downloader:
            print("No downloader selected.")
            return

        for d in downloads:
            url = d.get("download_url")
            if not url:
                logger.warning("Invalid download URL, skipping.")
                continue

            print(f"Downloading: {url}")
            try:
                if downloader.startswith("aria2"):
                    download_with_aria2(url)
                else:
                    download_with_wget(url)
            except Exception:
                logger.exception("Failed to download %s", url)

    except Exception:
        logger.exception("Error while choosing downloader")

def run_cli():
    try:
        selected = choose_from_search()
        downloads = choose_episodes(selected)
        choose_downloader_and_start(downloads)
    except Exception:
        logger.exception("Unexpected error in CLI run")
