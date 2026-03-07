import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

DOWNLOAD_PATH = os.path.expanduser(os.getenv("DOWNLOAD_PATH", "./downloads"))

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def download_with_aria2(url):
    subprocess.Popen([
        "aria2c",
        "--dir", DOWNLOAD_PATH,
        "--check-certificate=false",
        "-x", "16",
        "-s", "16",
        url
    ])


def download_with_wget(url):
    subprocess.run([
        "wget",
        "-c",
        "-nv",
        "--no-check-certificate",
        "-P", DOWNLOAD_PATH,
        url
    ])