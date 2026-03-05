# main.py
import subprocess
import questionary
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def run_searching(query):
    result = subprocess.run(
        ["python", "search.py", query],
        capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")
    search_results = []
    for line in lines:
        title, url = line.split("|||")
        search_results.append({"title": title, "url": url})
    return search_results

def run_episode(url):
    import subprocess

    result = subprocess.run(
        ["python", "episode.py", url],
        capture_output=True, text=True
    )

    lines = [line for line in result.stdout.strip().split("\n") if "|||" in line]

    episode_list = []
    for line in lines:
        number, ep_url = line.split("|||")
        episode_list.append({"number": number, "url": ep_url})

    return episode_list

if __name__ == "__main__":
    clear()
    query = input("Enter search term: ")

    search_results = run_searching(query)

    print("Results:\n")
    choices = [r["title"] for r in search_results]
    selected_title = questionary.select(
        "Choose result:",
        choices=choices
    ).ask()
    selected = next(r for r in search_results if r["title"] == selected_title)
    print(f"Selected: {selected['title']}\n{selected['url']}\n")

    episode_list = run_episode(selected["url"])

    print(f"Episodes for {selected['url']}:\n")
    for ep in episode_list:
        print(ep["number"])