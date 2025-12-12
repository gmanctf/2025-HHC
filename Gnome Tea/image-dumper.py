import os
import json
import re
import requests
from urllib.parse import urlparse

# Regex to match typical image URLs
IMAGE_REGEX = re.compile(
    r'(https?://[^\s\'"]+\.(?:png|jpg|jpeg|gif|webp|bmp|svg))',
    re.IGNORECASE
)

def extract_images(obj, image_set):
    """Recursively walk JSON and extract image URLs."""
    if isinstance(obj, dict):
        for v in obj.values():
            extract_images(v, image_set)

    elif isinstance(obj, list):
        for item in obj:
            extract_images(item, image_set)

    elif isinstance(obj, str):
        matches = IMAGE_REGEX.findall(obj)
        for m in matches:
            image_set.add(m)


def safe_filename_from_url(url):
    """Generate a safe filename from a URL."""
    path = urlparse(url).path
    name = os.path.basename(path)
    if not name:
        name = "unnamed"
    return name


def main():
    # --- Ask user for directory ---
    base_dir = input("Enter directory containing dump JSON files: ").strip()

    if not os.path.isdir(base_dir):
        print("[-] Not a valid directory.")
        return

    # --- Collect all .json files ---
    json_files = [f for f in os.listdir(base_dir) if f.lower().endswith(".json")]

    if not json_files:
        print("[-] No .json files found.")
        return

    print(f"[+] Found {len(json_files)} JSON files.")

    # Set to store deduplicated URLs
    image_urls = set()

    # --- Extract images from all JSON files ---
    for filename in json_files:
        file_path = os.path.join(base_dir, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[-] Error reading {filename}: {e}")
            continue

        extract_images(data, image_urls)

    print(f"[+] Extracted {len(image_urls)} unique image URLs.")

    # --- Prepare images directory ---
    out_dir = "images"
    os.makedirs(out_dir, exist_ok=True)

    # --- Download images ---
    print("[+] Downloading images...")
    downloaded = 0

    for url in image_urls:
        try:
            name = safe_filename_from_url(url)
            out_path = os.path.join(out_dir, name)

            # Skip if already downloaded
            if os.path.exists(out_path):
                print(f"[*] Already exists: {name}")
                continue

            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(out_path, "wb") as f:
                    f.write(r.content)
                print(f"[+] Downloaded: {name}")
                downloaded += 1
            else:
                print(f"[-] Failed ({r.status_code}): {url}")

        except Exception as e:
            print(f"[-] Error downloading {url}: {e}")

    print(f"\n[+] Done! Downloaded {downloaded} images.")
    print(f"[+] Saved in: {out_dir}")


if __name__ == "__main__":
    main()
