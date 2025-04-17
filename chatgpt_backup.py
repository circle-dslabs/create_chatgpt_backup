# ChatGPT Export to Markdown Converter
# - Uses conversations.json
# - Organizes by Year/Month folders
# - Links pre-downloaded images from export (files/ or images/)
# - Optionally zips the output folder

import os
import json
import re
from datetime import datetime
from zipfile import ZipFile

# === USER CONFIGURATION ===
INPUT_JSON = "conversations.json"            # Exported from ChatGPT ZIP
MARKDOWN_DIR = "markdown_chats"             # Output base directory
IMAGE_SUBFOLDER = "files"                   # Name of image folder in the export
ZIP_OUTPUT = True                            # Whether to create a ZIP archive
ZIP_NAME = "chatgpt_markdown_archive.zip"

# === UTILITY ===
def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name).strip().replace(' ', '_')

def link_images(text):
    # Replace placeholders like <file>abc.png</file> or raw filenames with markdown links
    return re.sub(r"<file>([^<]+)</file>", rf"![](../{IMAGE_SUBFOLDER}/\1)", text)

def convert_chats(json_path, output_dir, image_folder):
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, convo in enumerate(data.get("conversations", [])):
        messages = convo.get("mapping", {}).values()
        sorted_msgs = sorted(
            (m.get("message") for m in messages if m.get("message")),
            key=lambda m: m.get("create_time", 0)
        )

        if not sorted_msgs:
            continue

        # Organize by first message time
        first_time = sorted_msgs[0].get("create_time", 0)
        dt = datetime.fromtimestamp(first_time)
        year, month = dt.strftime('%Y'), dt.strftime('%B')
        convo_dir = os.path.join(output_dir, year, month)
        os.makedirs(convo_dir, exist_ok=True)

        title = sanitize_filename(convo.get("title", f"chat_{i}"))
        out_path = os.path.join(convo_dir, f"{title}.md")

        content = f"# {title}\n\n"
        for msg in sorted_msgs:
            role = msg.get("author", {}).get("role", "system")
            parts = msg.get("content", {}).get("parts", [""])
            ts = msg.get("create_time", 0)
            ts_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else "N/A"

            for part in parts:
                part = link_images(part)
                content += f"**{role.capitalize()} ({ts_str}):**\n\n{part.strip()}\n\n---\n\n"

        with open(out_path, 'w', encoding='utf-8') as out:
            out.write(content)

    print(f"✅ Converted {i+1} conversations to Markdown")

def zip_output(folder, zipname):
    with ZipFile(zipname, 'w') as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=os.path.dirname(folder))
                zipf.write(full_path, arcname)
    print(f"✅ Created ZIP archive: {zipname}")

# === MAIN ===
if __name__ == "__main__":
    convert_chats(INPUT_JSON, MARKDOWN_DIR, IMAGE_SUBFOLDER)
    if ZIP_OUTPUT:
        zip_output(MARKDOWN_DIR, ZIP_NAME)
