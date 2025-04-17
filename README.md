# ChatGPT Export to Markdown

This tool converts your exported ChatGPT chat history (`conversations.json`) into clean, timestamped Markdown files. It organizes them by year and month and links any embedded image or file references to corresponding files that already exist in your export folder.

---

## Features

- ✅ Converts `conversations.json` to `.md` files
- 📁 Organizes output as `markdown_chats/YYYY/Month/*.md`
- 🕓 Includes readable timestamps for each message
- 🖼️ Links pre-downloaded image/file references
- 📦 Optional: Create a zip archive of the final markdown folder

---

## Installation

```bash
pip install -r requirements.txt
```

> No dependencies are required for the basic conversion. If future enhancements are added (e.g., Google Drive upload), additional packages like `requests` or `PyDrive` may be included.

---

## Usage

```bash
python chatgpt_backup.py \
  --json conversations.json \
  --output markdown_chats \
  --image-folder files \
  --zip \
  --zip-name chatgpt_markdown_archive.zip
```

### Arguments
| Flag             | Default Value                     | Description                                      |
|------------------|------------------------------------|--------------------------------------------------|
| `--json`         | `conversations.json`               | Path to the exported chat JSON                   |
| `--output`       | `markdown_chats`                  | Output directory for markdown files              |
| `--image-folder` | `files`                           | Folder name containing image/file attachments    |
| `--zip`          | *(flag only)*                     | If set, zips the output folder                   |
| `--zip-name`     | `chatgpt_markdown_archive.zip`     | Name of the generated ZIP file                   |

---

## Example Folder Structure

```
chatgpt-markdown-archive/
├── markdown_chats/
│   └── 2025/
│       └── April/
│           └── My_Conversation.md
├── files/
│   └── uploaded_image.png
├── conversations.json
└── chatgpt_backup.py
```

---

## License

MIT License

