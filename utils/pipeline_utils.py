import subprocess

def run_pipeline(script, arg):
    result = subprocess.run(
        ["python", script, arg],
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split("\n")


def parse_pipe_lines(lines):
    return [line for line in lines if "|||" in line]


def run_searching(query):
    lines = run_pipeline("search_pipeline.py", query)
    search_results = []
    for line in lines:
        if "|||" in line:
            title, url = line.split("|||")
            search_results.append({"title": title, "url": url})
    return search_results


def run_episode(url):
    lines = parse_pipe_lines(run_pipeline("episode_pipeline.py", url))
    episode_list = []
    for line in lines:
        number, ep_url = line.split("|||")
        episode_list.append({"number": number, "url": ep_url})
    return episode_list


def run_download(urls):
    lines = parse_pipe_lines(run_pipeline("download_pipeline.py", urls))
    downloads = []
    for line in lines:
        ep_page, download_url = line.split("|||")
        downloads.append({"episode_page": ep_page, "download_url": download_url})
    return downloads