import os
import json
import re

def safe_filename(name):
    """
    Extract gnome name to be used as part of filename.
    Example: 'Grizelda Grit-Tooth' will be 'Grizelda-Grit-Tooth'
    """
    # Replace spaces with dashes
    name = name.replace(" ", "-")
    # Remove or replace characters that cannot be in filenames
    name = re.sub(r"[^A-Za-z0-9\-_]", "", name)
    return name


def extract_dms(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    out_dir = "dms"
    os.makedirs(out_dir, exist_ok=True)

    print(f"Found {len(conversations)} conversations.")

    for convo in conversations:
        fields = convo.get("fields", {})

        # ---- Get participant names ----
        participant_names_raw = (
            fields.get("participantNames", {})
            .get("arrayValue", {})
            .get("values", [])
        )

        participant_names = [v.get("stringValue", "Unknown")
                             for v in participant_names_raw]

        if len(participant_names) != 2:
            print("⚠️ Skipping conversation with unusual participant count.")
            continue

        p1, p2 = participant_names
        filename = f"{safe_filename(p1)}_and_{safe_filename(p2)}.txt"
        filepath = os.path.join(out_dir, filename)

        # ---- Messages ----
        messages_raw = (
            fields.get("messages", {})
            .get("arrayValue", {})
            .get("values", [])
        )

        lines = []
        for msg_entry in messages_raw:
            msg_fields = msg_entry.get("mapValue", {}).get("fields", {})

            sender = msg_fields.get("senderName", {}).get("stringValue", "Unknown")
            content = msg_fields.get("content", {}).get("stringValue", "")

            # JSON already decodes \u2014 properly → “—”
            lines.append(f"{sender}: {content}")

        # ---- Write conversation file ----
        with open(filepath, "w", encoding="utf-8") as out:
            out.write("\n".join(lines))

        print(f"[+] Saved: {filepath}")

def main():
    json_path = input("Enter path to the DM JSON file: ").strip()

    if not os.path.isfile(json_path):
        print("[-] File does not exist.")
        return

    extract_dms(json_path)
    print("\n[+] Done! DM conversations saved in ./dms/")


if __name__ == "__main__":
    main()
