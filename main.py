import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse

BASE_URL = "http://192.168.77.84:42069/Contributions/GhostOfTsushima/"
DOWNLOAD_DIR = "D:\\Games\\'Max Payne 3'"


def sanitize_path(path):
    return unquote(path).replace(":", "_").replace("?", "_").replace("*", "_")


def download_file(file_url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    print(f"Downloading: {file_url}")
    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading {file_url}: {e}")


visited = set()

def crawl_and_download(url, local_dir):
    if url in visited:
        return  # Already visited
    visited.add(url)

    print(f"Crawling: {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Failed to access {url}: {e}")
        return

    os.makedirs(local_dir, exist_ok=True)

    for link in soup.find_all("a"):
        href = link.get("href")
        if not href or href.startswith("?") or href.startswith("../") or href == "./":
            continue

        full_url = urljoin(url, href)
        decoded_name = sanitize_path(href)

        if not full_url.startswith(BASE_URL):
            continue

        if href.endswith("/"):
            sub_dir = os.path.join(local_dir, decoded_name)
            crawl_and_download(full_url, sub_dir)
        else:  
            local_path = os.path.join(local_dir, decoded_name)
            download_file(full_url, local_path)



if __name__ == "__main__":
    crawl_and_download(BASE_URL, DOWNLOAD_DIR)
    print("All downloads complete")
