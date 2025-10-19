# Document Processing System

A small FastAPI service that demonstrates using LangChain with Google Gemini (via `langchain_google_genai`) to build a document-processing API. The project includes a minimal FastAPI app that calls a Gemini model and example endpoints to extend for document processing tasks.

## Features
- FastAPI HTTP endpoints
- Integration with Google Gemini (via `langchain_google_genai` / LangChain)
- Environment-driven configuration for credentials
- Minimal starting point for document parsing, summarization, and QA flows

## Prerequisites
- Python 3.10+
- An environment with network access to Google AI services
- A Google API key or service account with access to Generative AI (Gemini) models
- pip (Python package installer)

## Recommended Gemini model ids
- `gemini-1.0`
- `gemini-1.5-pro`
- `gemini-2.5-flash`
Choose a model supported in your Google Cloud account.

## Installation
1. Clone the repo and change directory:
   ```bash
   git clone <repo-url>
   cd document-processing-system
   ```

2. Create and activate a virtual environment (macOS):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
   If `requirements.txt` is not present, install commonly used packages:
   ```bash
   python3 -m pip install fastapi uvicorn python-dotenv langchain-google-genai
   ```

## Configuration (.env)
Create a `.env` file at the project root (do NOT commit this file). Example `.env`:
```
GOOGLE_API_KEY=your_api_key_here
# or (recommended for production)
# GOOGLE_APPLICATION_CREDENTIALS=/full/path/to/service-account.json
```

Add `.env` to `.gitignore`:
```
.env
```

The app uses python-dotenv to load environment variables. Alternatively, set environment variables directly:
```bash
export GOOGLE_API_KEY="your_api_key_here"
# or for service account (recommended)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

## How to run
Start the FastAPI server with Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at: http://127.0.0.1:8000

## Example endpoints
- GET /  
  Calls the configured Gemini model with a simple prompt (demo).
  Example:
  ```bash
  curl http://127.0.0.1:8000/
  ```

- GET /items/{item_id}?q=optional  
  Demo endpoint for testing parameters.
  ```bash
  curl "http://127.0.0.1:8000/items/42?q=test"
  ```

## How the model is configured (example)
In `main.py` the recommended pattern is to read credentials from environment and create the model instance. Example snippet:
```python
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)
```
Do not hardcode keys in source.

## Extending for document processing
- Add endpoints to accept file uploads or URLs
- Use LangChain document loaders and retrievers (FAISS, Chroma) for retrieval-augmented generation
- Add tasks: OCR, text extraction, summarization, Q&A, metadata extraction

## Testing
- Add unit tests under `tests/` and run with pytest:
  ```bash
  python3 -m pip install pytest
  pytest
  ```

## Troubleshooting
- ValueError about inferring provider: ensure you are using the correct client class and passing credentials; prefer `google/...` model ids or use the `ChatGoogleGenerativeAI` class and `api_key` / ADC.
- Authentication errors: verify `GOOGLE_API_KEY` or `GOOGLE_APPLICATION_CREDENTIALS` and that billing/APIs are enabled in the Google Cloud Console.

## Security
- Never commit API keys or service account files.
- Use service accounts with least privilege for production.
- Rotate credentials regularly.

## Contributing
- Open issues or PRs for improvements. Write clear tests for new features.

## License
Add your project license here (e.g., MIT).