The python scripts can help in data collection for the `Gnome Tea` challenge from Holiday Hack Challenge 2025. The challenge was based on an application using Firebase to store content.

* `get-raw-collections.py`: Dump all the JSON data from all the collections. The script can also be used as a collection brute forcer as it get's the collection names from a text file and then try to access all of them.
* `image-dumper.py`: It parses all json files from the previous script to search for links to images, deduplicate entries, then downloads all images.
* `dm_extractor.py`: Takes as input for the user the dms.json file and extracts all conversations and saves them in the format `gnome1_and_gnome2.txt`. A great way to learn about gnome gossips and moon-gazing.

The folders contain the data that was extracted using the scripts.