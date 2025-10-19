from typing import Union
from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key =os.getenv("GOOGLE_API_KEY"))

@app.get("/")
def read_root():
    return model.invoke("hello, how are you?")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}