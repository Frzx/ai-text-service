from fastapi import FastAPI
from transformers import pipeline
from scalar_fastapi import get_scalar_api_reference
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from app.db import SessionDep, create_all_tables
from app.model import Sentiment
from app.schemas import AnalyzeRequest, AnalyzeResponse

load_dotenv()


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)


sentiment_pipeline = pipeline(
    task="sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/analyse", response_model=AnalyzeResponse)
async def analyse(
    payload: AnalyzeRequest,
    session: SessionDep,
):
    
    result = sentiment_pipeline(payload.text)
    label = result[0]["label"]
    sentiment = Sentiment(
        text=payload.text,
        label=label,
    )

    session.add(sentiment)
    await session.commit()
    await session.refresh(sentiment)
    return sentiment


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
