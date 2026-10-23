from random import choice

from fastapi import FastAPI, HTTPException, status, Query
from starlette.staticfiles import StaticFiles, FileResponse

import constants
from quote_service import ask_llm

from pathlib import Path

app = FastAPI(
    title="Quote API",
    description="An API that generates quotes using an LLM.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

BASE_DIR = Path(__file__).resolve().parent

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(BASE_DIR / "static" / "favicon.ico")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/quote")
@app.get("/")
def quote(subject: str | None = Query(default=None, min_length=1, max_length=100)):
    if not subject:
        subject = choice(constants.RANDOM_SUBJECT_LIST)

    subject = subject.strip().lower()

    quote_from_llm = ask_llm(subject)

    if quote_from_llm:
        return {
            "subject": subject,
            "quote": quote_from_llm
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Quote generation is temporarily unavailable"
        )

@app.api_route("/{path:path}", methods=["GET"])
def fallback_get(path: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Please try the '/' or the '/quote' endpoint."
    )

@app.api_route("/{path:path}", methods=["POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def fallback_other_methods(path: str):
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Please only use GET."
    )


