# GitHub Issue Analyzer

This project provides a web-based tool to automatically summarize and analyze GitHub issues using Large Language Models (LLMs) via the Hugging Face Inference API. It consists of a FastAPI backend and a Streamlit frontend. Users can input a public GitHub repository URL and issue number to receive a structured analysis of the issue, including a summary, classification, priority scoring, and label suggestions.

---

## Features

- Fetches issue title, body, and comments directly from GitHub
- Sends the data to a Hugging Face-hosted LLM model
- Returns a structured JSON response with detailed insights
- Built with Python, FastAPI, Streamlit, and Hugging Face Inference API

---

## Prerequisites

- Python 3.8 or higher
- A Hugging Face API key (free tier is sufficient)

You can generate a Hugging Face API token from:  
[https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## Project Structure

github-issue-analyzer/
├── backend/
│ ├── main.py # FastAPI backend
│ ├── .env # API key (not committed)
│ └── requirements.txt
├── frontend/
│ ├── app.py # Streamlit frontend
│ └── requirements.txt
├── README.md
└── .gitignore


---

## Setup Instructions (Complete in Under 5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/github-issue-analyzer.git
cd github-issue-analyzer


2. Configure API Key
Create a .env file inside the backend/ directory with the following content:
HUGGINGFACE_API_KEY=your_huggingface_token_here


3. Run the Backend (FastAPI)
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
API will be available at: http://localhost:8000


4. Run the Frontend (Streamlit)
In a new terminal window:
cd frontend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
Interface will open at: http://localhost:8501


Example Input
You can test with a public GitHub issue:
Repository URL: https://github.com/streamlit/streamlit
Issue Number: 6261

Expected Output Format
The output will be a structured JSON like:
{
"summary":" Webrtc live video loading has stop working . I tried deploying my app yesterday and the live video loaded fine . But today I get errors and live video could not load . I checked back on this component page - it has the same error . I have provided sufficient information below to help reproduce this issue ."
"title":"webrtc unable to load live video"
"url":"https://github.com/streamlit/streamlit/issues/6261"
"state":"closed"
}


Technologies Used
FastAPI for backend API
Streamlit for frontend UI
Hugging Face Inference API
GitHub REST API
Python 3.8+


Acknowledgements
Hugging Face
FastAPI
Streamlit
GitHub REST API





