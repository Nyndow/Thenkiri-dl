import subprocess
from dotenv import load_dotenv
import os
import logging

load_dotenv()

DOWNLOAD_PATH = os.path.expanduser(os.getenv("DOWNLOAD_PATH", "./downloads"))

os.makedirs(DOWNLOAD_PATH, exist_ok=True)
logger = logging.getLogger(__name__)

def download_with_aria2(url):
    try:
        subprocess.run([
            "aria2c",
            "--dir", DOWNLOAD_PATH,              
            "-x", "3",                       
            "-s", "3",                            
            "--summary-interval=1",           
            url
        ], check=True)  # raises exception if download fails
    except subprocess.CalledProcessError:
        logger.exception("Download failed for %s", url)


def download_with_wget(url):
    try:
        subprocess.run([
            "wget",
            "-c",  # continue if partially downloaded
            "-P", DOWNLOAD_PATH,
            "--progress=bar:force",
            url
        ], check=True)
    except subprocess.CalledProcessError:
        logger.exception("Download failed for %s", url)
