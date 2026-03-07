import os
import questionary
from utils.pipeline_utils import run_searching, run_episode, run_download
from utils.download_utils import download_with_aria2, download_with_wget

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def choose_from_search():
    clear()
    query = input("Enter search term: ")
    search_results = run_searching(query)

    print("\nResults:\n")
    choices = [r["title"] for r in search_results]

    selected_title = questionary.select(
        "Choose result:",
        choices=choices
    ).ask()

    selected = next(r for r in search_results if r["title"] == selected_title)
    print(f"\nSelected: {selected['title']}")
    print(selected["url"])
    return selected


def choose_episodes(selected):
    episode_list = run_episode(selected["url"])

    if not episode_list:
        print(f"No episodes found for {selected['title']}")
        return []

    print(f"\nEpisodes for {selected['url']}:\n")

    # Only one episode? Ask confirmation instead of checkbox
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
            "Select episodes (use TAB or SPACE to select multiple):",
            choices=choices
        ).ask()

        if not selected_episode_urls:
            print("No episodes selected.")
            return []

        episode_urls = ",".join(selected_episode_urls)

    downloads = run_download(episode_urls)
    return downloads


def choose_downloader_and_start(downloads):
    downloader = questionary.select(
        "Choose downloader:",
        choices=[
            "aria2 (fast multi-connection)",
            "wget (simple downloader)"
        ]
    ).ask()

    for d in downloads:
        url = d["download_url"]
        print(url)
        if downloader.startswith("aria2"):
            download_with_aria2(url)
        else:
            download_with_wget(url)


def run_cli():
    selected = choose_from_search()
    downloads = choose_episodes(selected)
    choose_downloader_and_start(downloads)