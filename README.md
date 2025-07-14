# 🧠 GitHub Issue Analyzer with LLM (FastAPI + Streamlit)

This project analyzes GitHub issues using an AI model from Hugging Face and generates a concise summary using real-time GitHub issue data.

---

## 📸 Demo

> Paste a GitHub issue URL → See an AI-generated summary within seconds!

![screenshot](https://github.com/yourusername/github-issue-analyzer/assets/demo.gif)

---

## 🚀 Features

- 🧵 Fetches issue title, body, and comments from **any public GitHub repository**
- 🤖 Uses **Hugging Face summarization model** (DistilBART) to analyze and generate a smart summary
- ⚡ Built with:
  - FastAPI for the backend API
  - Streamlit for the frontend interface
  - Hugging Face Inference API for AI generation

---

## 🛠️ Installation & Setup (⏱️ Under 5 Minutes)

### 📁 1. Clone the Repository

```bash
git clone https://github.com/yourusername/github-issue-analyzer.git
cd github-issue-analyzer



github-issue-analyzer/
├── backend/
│   ├── main.py              # FastAPI backend logic
│   ├── requirements.txt
│   └── .env                 # (not pushed to GitHub)
│
├── frontend/
│   ├── app.py               # Streamlit frontend
│   └── requirements.txt
│
├── README.md
└── .gitignore



📄 Technologies Used
FastAPI (Backend API)
Streamlit (Frontend UI)
Hugging Face Inference API
GitHub REST API (v3)
Python 3.8+



Developed by Namrutha M
Special thanks to Hugging Face and GitHub API!!!


