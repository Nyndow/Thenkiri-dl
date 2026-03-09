import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

DOWNLOAD_PATH = os.path.expanduser(os.getenv("DOWNLOAD_PATH", "./downloads"))

os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def download_with_aria2(url):
    try:
        subprocess.run([
            "aria2c",
            "--dir", DOWNLOAD_PATH,          
            "--check-certificate=false",      
            "-x", "16",                       
            "-s", "16",                            
            "--summary-interval=1",           
            url
        ], check=True)  # raises exception if download fails
    except subprocess.CalledProcessError as e:
        print(f"Download failed for {url}: {e}")


def download_with_wget(url):
    try:
        subprocess.run([
            "wget",
            "-c",  # continue if partially downloaded
            "--no-check-certificate",
            "-P", DOWNLOAD_PATH,
            "--progress=bar:force",
            url
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Download failed for {url}: {e}")