import os
import questionary
from utils.pipeline_utils import run_searching, run_episode, run_download
from utils.download_utils import download_with_aria2, download_with_wget

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def choose_from_search():
    try:
        clear()
        query = input("Search for a show: ")
        search_results = run_searching(query)

        if not search_results:
            print("No results found for your search.")
            return None

        print("\nResults:\n")
        choices = [r["title"] for r in search_results]

        selected_title = questionary.select(
            "Choose result:",
            choices=choices
        ).ask()

        if not selected_title:
            print("No selection made.")
            return None

        selected = next(r for r in search_results if r["title"] == selected_title)
        print(f"\nSelected: {selected['title']}")
        print(selected["url"])
        return selected

    except Exception as e:
        print(f"An error happened during search: {e}")
        return None

def choose_episodes(selected):
    if not selected:
        return []

    try:
        episode_list = run_episode(selected["url"])

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
                questionary.Choice(title=f"Episode {ep['number']}", value=ep["url"])
                for ep in episode_list
            ]
            selected_episode_urls = questionary.checkbox(
                "Select episodes (use SPACE to select multiple):",
                choices=choices
            ).ask()

            if not selected_episode_urls:
                print("No episodes selected.")
                return []

            episode_urls = ",".join(selected_episode_urls)

        downloads = run_download(episode_urls)
        return downloads

    except Exception as e:
        print(f"An error happened while selecting episodes: {e}")
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
                print("Invalid download URL, skipping.")
                continue

            print(f"Downloading: {url}")
            try:
                if downloader.startswith("aria2"):
                    download_with_aria2(url)
                else:
                    download_with_wget(url)
            except Exception as e:
                print(f"Failed to download {url}: {e}")

    except Exception as e:
        print(f"An error happened while choosing downloader: {e}")

def run_cli():
    try:
        selected = choose_from_search()
        downloads = choose_episodes(selected)
        choose_downloader_and_start(downloads)
    except Exception as e:
        print(f"An unexpected error happened: {e}")