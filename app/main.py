from fastapi import FastAPI
from transformers import pipeline
from scalar_fastapi import get_scalar_api_reference

from dotenv import load_dotenv()

app = FastAPI()


sentiment_pipeline = pipeline(task = "sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/analyse")
def analyse(text: str):
    result = sentiment_pipeline(text)
    return result[0]["label"]


@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
    