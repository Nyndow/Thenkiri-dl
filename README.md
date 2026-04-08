# Thenkiri-dl

**Thenkiri-dl** is a CLI tool designed to download videos from  
https://Thenkiri.com quickly and easily.

It uses **aria2** and/or **wget** to ensure fast and reliable downloads.

---

## Features

- Search shows available on **Thenkiri** and **Dramakey** 
- Select episodes directly from the terminal
- Download using **aria2** or **wget**
- Resume interrupted downloads *(download links remain active for ~8 hours)*
- Simple CLI interface

---

## Installation

Choose the installation method that fits your environment.

---

### 🐳 Docker Hub image

Pull the published image from Docker Hub:
```bash
docker pull nyndow/thenkiri-dl:latest
```

Run it with a named volume for downloads:
```bash
docker run -it -v thenkiri_downloads:/downloads nyndow/thenkiri-dl:latest
```

Access a shell inside the container:
```bash
docker run -it nyndow/thenkiri-dl:latest bash
```

---

### 🔧 Local Docker installation

This project includes a `Dockerfile` so you can run Thenkiri-dl without installing Python or dependencies locally.

#### Build the Docker image locally
```bash
docker build -t thenkiri-dl .
```

#### Run the container locally
```bash
docker run -it thenkiri-dl
```

#### Run with local download and log folders

To keep downloaded files and logs outside the container, mount local directories:
```bash
docker run -it \
  -v "$PWD/downloads:/downloads" \
  -v "$PWD/logs:/app/logs" \
  thenkiri-dl
```

#### Override Docker environment variables
```bash
docker run -it \
  -e DOWNLOAD_PATH=/downloads \
  -e THENKIRI_LOG_PATH=/app/logs/thenkiri.log \
  -v "$PWD/downloads:/downloads" \
  -v "$PWD/logs:/app/logs" \
  thenkiri-dl
```

---

### 🛠️ Manual installation

Make sure you have **aria2** and/or **wget** installed on your system.

#### Clone the repository
```bash
git clone https://github.com/Nyndow/Thenkiri-dl
cd Thenkiri-dl
pip install -r requirements.txt
```

Create a `.env` file at the root of the directory and add:
```bash
DOWNLOAD_PATH=~/Videos/Thenkiri-dl
```

To run:
```bash 
cd src
python main.py
```

---

## Usage

### Search for the show
![Searching for a show](assets/search.png)

### Select the episodes you wish to download
![Selecting episodes](assets/select-episodes.png)

### Download by choosing wget or aria2
![Choosing download method](assets/download.png)

---

## Disclaimer

This project is created for educational purposes only.  
I am not affiliated with Thenkiri.com.  
Use this tool responsibly and respect the website's terms of service.
