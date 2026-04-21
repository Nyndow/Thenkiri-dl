import subprocess
import os
import logging
import re
from dotenv import load_dotenv

from utils.settings_utils import load_settings

load_dotenv()

raw_path = os.getenv("DOWNLOAD_PATH", "./downloads")
DOWNLOAD_PATH = os.path.abspath(os.path.expanduser(raw_path))
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

logger = logging.getLogger(__name__)


# ---------------------------
# Helpers
# ---------------------------

def sanitize(name: str) -> str:
    """Remove illegal filesystem characters."""
    return re.sub(r'[\\/*?:"<>|]', "", name or "default")


def ask_user(prompt: str) -> bool:
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer in ["y", "yes"]


def get_target_dir(folder_name: str | None) -> str:
    """Resolve final download directory."""
    if not folder_name:
        return DOWNLOAD_PATH

    path = os.path.join(DOWNLOAD_PATH, sanitize(folder_name))
    os.makedirs(path, exist_ok=True)
    return path

# Aria2 downloader

def download_with_aria2(url, folder_name=None, insecure=None):
    settings = load_settings()
    if insecure is None:
        insecure = settings.get("no_certificate_check", False)

    target_dir = get_target_dir(folder_name)

    cmd = [
        "aria2c",
        "--dir", target_dir,
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
                download_with_aria2(url, folder_name=folder_name, insecure=True)


# Wget downloader

def download_with_wget(url, folder_name=None, insecure=None):
    settings = load_settings()
    if insecure is None:
        insecure = settings.get("no_certificate_check", False)

    target_dir = get_target_dir(folder_name)

    cmd = [
        "wget",
        "-c",
        "-P", target_dir,
        "--progress=bar:force:noscroll",
    ]

    if insecure:
        cmd.append("--no-check-certificate")

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)

    except subprocess.CalledProcessError as e:
        logger.exception("wget download failed for %s", url)

        error_text = (e.stderr or "").lower() if e.stderr else ""
        is_ssl_error = "certificate" in error_text or "ssl" in error_text

        if is_ssl_error and not insecure:
            print("\nSSL certificate error detected (wget).")

            if ask_user("Continue without certificate verification?"):
                download_with_wget(url, folder_name=folder_name, insecure=True)