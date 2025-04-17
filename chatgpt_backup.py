import os
import json
import re
import requests
from zipfile import ZipFile
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def sanitize_filename(title):
    return "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in title).strip().replace(" ", "_")


def extract_and_download_images(content, image_dir):
    os.makedirs(image_dir, exist_ok=True)
    image_urls = re.findall(r'https://[^"\s]+?\.(?:png|jpg|jpeg|gif)', content)
    replacements = {}
    for url in image_urls:
        try:
            ext = url.split(".")[-1].split("?")[0]
            img_name = f"image_{len(os.listdir(image_dir))}.{ext}"
            img_path = os.path.join(image_dir, img_name)
            if not os.path.exists(img_path):  # Avoid duplicates
                r = requests.get(url)
                with open(img_path, "wb") as f:
                    f.write(r.content)
            replacements[url] = f"images/{img_name}"
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    return replacements


def convert_chats(json_path, base_output_dir="markdown_chats", image_dir="images"):
    os.makedirs(base_output_dir, exist_ok=True)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, convo in enumerate(data["conversations"]):
        messages = convo.get("mapping", {}).values()
        sorted_msgs = sorted(
            (m.get("message") for m in messages if m.get("message")),
            key=lambda m: m.get("create_time", 0)
        )

        if not sorted_msgs:
            continue

        title = sanitize_filename(convo.get("title", f"chat_{i}"))
        timestamp = sorted_msgs[0].get("create_time", 0)
        dt = datetime.fromtimestamp(timestamp)
        year_folder = dt.strftime('%Y')
        month_folder = dt.strftime('%B')
        output_dir = os.path.join(base_output_dir, year_folder, month_folder)
        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, f"{title}.md")
        all_text = f"# {title}\n\n"
        for msg in sorted_msgs:
            role = msg.get("author", {}).get("role", "system")
            parts = msg.get("content", {}).get("parts", [""])
            ts = msg.get("create_time", 0)
            ts_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else "N/A"

            for part in parts:
                replacements = extract_and_download_images(part, image_dir)
                for url, local_path in replacements.items():
                    part = part.replace(url, local_path)
                all_text += f"**{role.capitalize()} ({ts_str}):**\n\n{part.strip()}\n\n---\n\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(all_text)

    print(f"✅ Converted {len(data['conversations'])} chats to Markdown (by year/month).")


def zip_backup(zip_name="chatgpt_backup.zip", folders=["markdown_chats", "images"]):
    with ZipFile(zip_name, "w") as zipf:
        for folder in folders:
            for root, _, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, ".")
                    zipf.write(full_path, arcname)
    print(f"✅ Zipped backup to {zip_name}")
    return zip_name


def upload_to_drive(file_path):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("token.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("token.json")

    drive = GoogleDrive(gauth)
    file_drive = drive.CreateFile({'title': os.path.basename(file_path)})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    print(f"✅ Uploaded to Google Drive: {file_drive['alternateLink']}")


if __name__ == "__main__":
    json_file = "conversations.json"
    convert_chats(json_file)
    archive = zip_backup()
    upload_to_drive(archive)
