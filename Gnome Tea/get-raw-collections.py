import requests
import json
import os
import sys

def read_collection_list(path):
    """
    Reads user-supplied list of collections.
    Ignores blank lines and comments starting with #.
    """
    if not os.path.exists(path):
        print(f"[!] Collection list file not found: {path}")
        sys.exit(1)

    with open(path, "r") as f:
        lines = f.read().splitlines()

    collections = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        collections.append(line)

    return collections


def fetch_collection(page_url):
    """
    Fetches one page of documents for a collection.
    Returns tuple: (documents_list, nextPageToken_or_None)
    """
    r = requests.get(page_url)

    if r.status_code == 404:
        # no such collection
        return None, None

    if r.status_code != 200:
        print(f"[!] Error fetching {page_url} : {r.text}")
        return None, None

    data = r.json()
    docs = data.get("documents", [])
    token = data.get("nextPageToken")

    return docs, token


def dump_collection(project, collection, outdir):
    """
    Fetches all pages for one collection and dumps them to JSON.
    """

    base = f"https://firestore.googleapis.com/v1/projects/{project}/databases/(default)/documents/{collection}"
    all_docs = []

    print(f"[*] Fetching collection: {collection}")

    url = base
    while True:
        docs, token = fetch_collection(url)

        if docs is None:
            print(f"[!] Skipping invalid or inaccessible collection: {collection}")
            return

        all_docs.extend(docs)

        if not token:
            break

        url = base + f"?pageToken={token}"

    # save
    outfile = os.path.join(outdir, f"{collection}.json")
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, indent=2)

    print(f"[+] Saved {len(all_docs)} docs → {outfile}")


def main():
    print("=== Firebase Firestore Dump (User-Supplied Collections) ===")

    project = input("Enter Firebase Project ID (e.g. holidayhack2025): ").strip()
    collection_file = input("Enter collection list filename (e.g. collections.txt): ").strip()

    collections = read_collection_list(collection_file)

    if not collections:
        print("[!] No valid collection names found.")
        sys.exit(1)

    print(f"[+] Loaded {len(collections)} collections from list.")

    outdir = f"firestore_dump_{project}"
    os.makedirs(outdir, exist_ok=True)

    for col in collections:
        dump_collection(project, col, outdir)

    print("\n[✓] Completed Firestore dump.")


if __name__ == "__main__":
    main()
