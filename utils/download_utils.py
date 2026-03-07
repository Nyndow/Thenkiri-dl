import subprocess

def download_with_aria2(url):
    subprocess.Popen([
        "aria2c",
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
        url
    ])