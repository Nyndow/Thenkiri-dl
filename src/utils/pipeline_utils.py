import subprocess
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

def run_pipeline(script, arg):
    src_dir = Path(__file__).resolve().parent.parent
    script_path = src_dir / script
    result = subprocess.run(
        [sys.executable, str(script_path), arg],
        capture_output=True,
        text=True,
        cwd=str(src_dir)
    )
    stdout_lines = result.stdout.strip().split("\n") if result.stdout else []
    stderr_text = result.stderr.strip() if result.stderr else ""
    if result.returncode != 0:
        logger.error(
            "Pipeline %s failed with code %s. Stderr: %s",
            script,
            result.returncode,
            stderr_text
        )
    return stdout_lines, stderr_text, result.returncode


def parse_pipe_lines(lines):
    return [line for line in lines if "|||" in line]


def run_searching(query):
    lines, stderr_text, returncode = run_pipeline("search_pipeline.py", query)
    if returncode != 0:
        logger.error("Search pipeline failed for query=%s. Stderr: %s", query, stderr_text)
        return None
    search_results = []
    for line in lines:
        if "|||" in line:
            title, url = line.split("|||")
            search_results.append({"title": title, "url": url})
    return search_results


def run_episode(url):
    lines, stderr_text, returncode = run_pipeline("episode_pipeline.py", url)
    if returncode != 0:
        logger.error("Episode pipeline failed for url=%s. Stderr: %s", url, stderr_text)
        return None
    lines = parse_pipe_lines(lines)
    episode_list = []
    for line in lines:
        number, ep_url = line.split("|||")
        episode_list.append({"number": number, "url": ep_url})
    return episode_list


def run_download(urls):
    lines, stderr_text, returncode = run_pipeline("download_pipeline.py", urls)
    if returncode != 0:
        logger.error("Download pipeline failed for urls=%s. Stderr: %s", urls, stderr_text)
        return None
    lines = parse_pipe_lines(lines)
    downloads = []
    for line in lines:
        ep_page, download_url = line.split("|||")
        downloads.append({"episode_page": ep_page, "download_url": download_url})
    return downloads
