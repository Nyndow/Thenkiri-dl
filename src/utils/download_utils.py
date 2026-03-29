import subprocess
from dotenv import load_dotenv
import os
import logging

load_dotenv()

raw_path = os.getenv("DOWNLOAD_PATH", "./downloads")
DOWNLOAD_PATH = os.path.abspath(os.path.expanduser(raw_path))
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

logger = logging.getLogger(__name__)


def ask_user(prompt: str) -> bool:
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer in ["y", "yes"]


# aria2 download
def download_with_aria2(url, insecure=False):
    cmd = [
        "aria2c",
        "--dir", DOWNLOAD_PATH,
        "-x", "3",
        "-s", "3",
        "--summary-interval=1",
    ]

    if insecure:
        cmd.append("--check-certificate=false")

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        logger.exception("aria2 download failed for %s", url)

        if not insecure:
            print("\nSSL certificate error detected (aria2).")

            if ask_user("Continue without certificate verification?"):
                download_with_aria2(url, insecure=True)


# wget download
def download_with_wget(url, insecure=False):
    cmd = [
        "wget",
        "-c",
        "-P", DOWNLOAD_PATH,
        "--progress=bar:force",
    ]

    if insecure:
        cmd.append("--no-check-certificate")

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        logger.exception("wget download failed for %s", url)

        error_text = (e.stderr or "").lower()
        is_ssl_error = "certificate" in error_text or "ssl" in error_text

        if is_ssl_error and not insecure:
            print("\nSSL certificate error detected (wget).")

            if ask_user("Continue without certificate verification?"):
                download_with_wget(url, insecure=True)