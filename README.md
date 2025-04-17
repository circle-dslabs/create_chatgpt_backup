# 📝 ChatGPT Markdown Archive Tool

This open-source tool converts your exported **ChatGPT chat history** into a set of clean, timestamped **Markdown files**, automatically downloads any **referenced/generated images**, organizes everything into a **Year/Month folder structure**, **zips the result**, and optionally **uploads the backup to your Google Drive**.

---

## ✅ Features

- 📁 Converts all exported ChatGPT chats into individual `.md` files
- 🥓 Adds readable timestamps for each message
- 🖼️ Downloads all image URLs (uploaded files, DALL·E images, etc.)
- 📂 Automatically organizes files into `markdown_chats/YYYY/Month/`
- 📆 Creates a zip archive `chatgpt_backup.zip`
- ☁️ Uploads backup to your **Google Drive** via API
- 🔐 Stores Google Drive token for reuse (`token.json`)
- 🗖️ **Monthly automation** via included GitHub Actions workflow

---

## 🚀 Quick Start

### 1. 🔄 Export Your Data from ChatGPT

1. Go to ChatGPT > Settings > **Data Controls**
2. Click **Export Data**
3. You’ll get a ZIP file via email
4. Unzip it, and copy `conversations.json` into this folder

---

### 2. 🔧 Set Up Google Drive API (One-Time Setup)

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (e.g., `ChatGPT Backup Tool`)
3. Enable the **Google Drive API** in the "APIs & Services" panel
4. Go to **Credentials** > Create Credentials > **OAuth 2.0 Client ID**
   - Application type: **Desktop**
5. Download the `client_secret_XXXX.json` file
6. Rename it to: `client_secrets.json`
7. Place it in your project folder (same level as the script)

---

### 3. 📅 Install Python Dependencies

Make sure you have Python 3.7+ installed, then run:

```bash
pip install -r requirements.txt
```

---

### 4. 🛠️ Run the Backup Script

```bash
python3 chatgpt_backup.py
```

- First run will open a browser for Google login
- Token will be saved as `token.json` and reused automatically

---

## 📂 Output Structure

After running the script, your folder will contain:

```
chatgpt_backup.zip
markdown_chats/
└── 2025/
    └── April/
        └── My_Chat_Title.md
images/
└── image_0.png
```

---

## ⚙️ GitHub Actions: Monthly Auto Backup

We’ve included a GitHub Actions workflow that runs the script automatically on the 1st of every month.

### 🔄 Setup (Optional)

1. Add this repo to GitHub
2. Commit your code, excluding secrets (they're in `.gitignore`)
3. If you want to automate backup:
   - Store `client_secrets.json` and `token.json` securely
   - Inject them as GitHub Secrets or use encrypted artifacts

> 🔐 This step is optional and **advanced**. Manual runs are safer for most users.

---

## 🔐 Auth Token Management

- First time you run the script, it will open a browser to log into Google.
- After login, a `token.json` is saved and reused (handled by `settings.yaml`).
- You can delete this file to revoke access or re-authenticate.

---

## 📁 Files Included

| File/Folder                | Purpose                                |
|---------------------------|----------------------------------------|
| `chatgpt_backup.py`       | Main script for markdown conversion & upload |
| `requirements.txt`        | Python packages needed                 |
| `settings.yaml`           | Configures Google Drive token behavior |
| `.github/workflows/...`   | GitHub Actions workflow for monthly backup |
| `.gitignore`              | Prevents committing secrets & outputs |
| `README.md`               | You’re reading it!                     |
| `LICENSE`                 | MIT license for reuse                  |

---

## 💡 Tips

- You can upload the resulting `chatgpt_backup.zip` to Google Drive, Dropbox, or S3
- You can modify the script to:
  - Combine all chats into a single `.md` file
  - Generate `.pdf` instead of markdown
  - Backup to other storage platforms

---

## 🥪 License

This project is licensed under the **MIT License**.

Feel free to modify, fork, and reuse it for personal or commercial use.

---

## 🤝 Contributions & Feedback

Got a feature request? Found a bug?  
Feel free to [open an issue](https://github.com/YOUR_ORG/chatgpt-markdown-archive/issues) or submit a pull request!

---

