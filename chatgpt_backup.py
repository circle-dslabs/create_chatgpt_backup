import os
import json
import re
import base64
import argparse
from datetime import datetime
from zipfile import ZipFile

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name).strip().replace(' ', '_')

def embed_images(text, image_base_path):
    def replacer(match):
        filename = match.group(1)
        filepath = os.path.join(image_base_path, filename)
        if not os.path.exists(filepath):
            return f"**[Missing file: {filename}]**"
        ext = os.path.splitext(filename)[-1][1:].lower()
        mime = f"image/{ext if ext != 'jpg' else 'jpeg'}"
        with open(filepath, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode('utf-8')
        return f"![{filename}](data:{mime};base64,{b64_data})"

    return re.sub(r"<file>([^<]+)</file>", replacer, text)

def convert_chats(json_path, output_dir, image_folder):
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, convo in enumerate(data):
        messages = convo.get("mapping", {}).values()
        sorted_msgs = sorted(
            (m.get("message") for m in messages if m.get("message")),
            key=lambda m: m.get("create_time", 0)
        )

        if not sorted_msgs:
            continue

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
                part = embed_images(part, image_folder)
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert ChatGPT export to Markdown with embedded images")
    parser.add_argument("--json", default="conversations.json", help="Path to conversations.json")
    parser.add_argument("--output", default="markdown_chats", help="Output folder for markdown")
    parser.add_argument("--image-folder", default=".", help="Folder where exported images/files are stored")
    parser.add_argument("--zip", action="store_true", help="If set, zip the output folder")
    parser.add_argument("--zip-name", default="chatgpt_markdown_archive.zip", help="Name of the zip archive to create")
    args = parser.parse_args()

    convert_chats(args.json, args.output, args.image_folder)
    if args.zip:
        zip_output(args.output, args.zip_name)
