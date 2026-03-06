import subprocess
import questionary
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def run_searching(query):
    result = subprocess.run(
        ["python", "search.py", query],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().split("\n")

    search_results = []
    for line in lines:
        if "|||" in line:
            title, url = line.split("|||")
            search_results.append({
                "title": title,
                "url": url
            })

    return search_results


def run_episode(url):
    result = subprocess.run(
        ["python", "episode.py", url],
        capture_output=True,
        text=True
    )

    lines = [line for line in result.stdout.strip().split("\n") if "|||" in line]

    episode_list = []
    for line in lines:
        number, ep_url = line.split("|||")
        episode_list.append({
            "number": number,
            "url": ep_url
        })

    return episode_list


def run_download(urls):
    result = subprocess.run(
        ["python", "download.py", urls],
        capture_output=True,
        text=True
    )

    lines = [line for line in result.stdout.strip().split("\n") if "|||" in line]

    downloads = []
    for line in lines:
        ep_page, download_url = line.split("|||")
        downloads.append({
            "episode_page": ep_page,
            "download_url": download_url
        })

    return downloads


if __name__ == "__main__":

    clear()

    query = input("Enter search term: ")

    #Searching
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


    # Episode list
    episode_list = run_episode(selected["url"])

    print(f"\nEpisodes for {selected['url']}:\n")

    for ep in episode_list:
        print(ep["number"], ep["url"])


    episode_urls = ",".join([ep["url"] for ep in episode_list])


    # Download links
    downloads = run_download(episode_urls)


    #Downloader choice
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
            subprocess.Popen([
                "aria2c",
                "-x", "16",
                "-s", "16",
                url
            ])

        else:
            subprocess.run([
                "wget",
                "-c",                     # continue incomplete downloads
                "-nv",                    # less verbose
                "--no-check-certificate", # ignore certificate errors
                url
            ])