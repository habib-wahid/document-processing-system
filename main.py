import tempfile
from typing import Union
from fastapi import FastAPI, HTTPException, UploadFile
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = FastAPI()
logger = logging.getLogger(__name__)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key =os.getenv("GOOGLE_API_KEY"))



@app.get("/")
def read_root():
    return model.invoke("hello, how are you?")


@app.post("/files")
async def upload_file(file: UploadFile):

    logger.info(f"Received file1: {file.filename}")

    print(f"Received file: {file.filename}")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()

        print(f"Loaded {len(docs[0].page_content)} pages from the PDF.")


        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap  = 50,
            add_start_index = True
        )

        all_texts = text_splitter.split_documents(docs)

        print(f"Split into {len(all_texts)} chunks.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        # Here you can process texts with the model or store them as needed
    return {"filename": file.filename}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}