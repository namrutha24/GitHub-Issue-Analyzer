from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from typing import Tuple, List, Dict, Any
import requests
import json
import re

# Load environment variables from a .env file
load_dotenv()

# Get the Hugging Face API key from environment variables
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if HF_API_KEY:
    print(f"Hugging Face API Key loaded successfully, starting with: {HF_API_KEY[:5]}...")
else:
    print("CRITICAL: Hugging Face API Key not found. Please ensure it is set in the .env file.")

# Using the summarization model as requested
HF_MODEL = "sshleifer/distilbart-cnn-12-6"

# Initialize the FastAPI application
app = FastAPI()

# Pydantic model for the request body
class AnalyzeRequest(BaseModel):
    repo_url: str
    issue_number: int

def build_prompt(issue: Dict[str, Any], comments: List[Dict[str, Any]]) -> str:
    """Constructs a prompt suitable for a summarization model."""
    comments_text = "\n\n".join([
        f"Comment by {c['user']['login']}: {c['body']}"
        for c in comments
        if c.get('body')
    ][:5])

    # The prompt is simplified to just provide the text to be summarized.
    # This matches the capability of the distilbart model.
    return f"""
ISSUE TITLE: {issue.get('title', '')}
ISSUE BODY: {issue.get('body', '')}
COMMENTS: {comments_text if comments_text else 'No comments'}
"""

async def fetch_github_issue(owner: str, repo: str, issue_number: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetches a specific issue and its comments from the GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(url)
            r.raise_for_status()
            issue = r.json()
            
            comments = []
            if issue.get("comments_url"):
                cr = await client.get(issue["comments_url"])
                if cr.status_code == 200:
                    comments = cr.json()
            return issue, comments
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="GitHub issue not found or access denied.")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to GitHub: {e}")


def call_huggingface(prompt: str) -> Dict[str, Any]:
    """Calls the Hugging Face Inference API and handles summarization output."""
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        # No extra parameters needed for this model
    }

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            error_msg = f"Hugging Face API error ({response.status_code}): {response.text}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        result = response.json()
        
        # This logic is updated to handle the output of a summarization model.
        if isinstance(result, list) and result:
            # Summarization models often return 'summary_text'
            summary = result[0].get("summary_text", "")
            return {"summary": summary}
        else:
            return {"error": "Failed to get a valid summary from AI model.", "raw_response": result}
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

    
@app.post("/analyze")
async def analyze_issue(request: AnalyzeRequest) -> Any:
    """The main API endpoint to analyze a GitHub issue."""
    try:
        parts = request.repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid repository URL format.")
        owner, repo = parts[-2], parts[-1]
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid repository URL format. Use format like 'https://github.com/owner/repo'.")

    # Fetch the issue data from GitHub
    issue, comments = await fetch_github_issue(owner, repo, request.issue_number)
    
    # Build the prompt and get the AI summary
    prompt = build_prompt(issue, comments)
    analysis_result = call_huggingface(prompt)

    # If the AI call resulted in an error, return it directly
    if "error" in analysis_result:
        return analysis_result

    # Combine the AI summary with data from the original issue
    final_response = {
        "summary": analysis_result.get("summary"),
        "title": issue.get("title"),
        "url": issue.get("html_url"),
        "state": issue.get("state")
    }
    
    return final_response
