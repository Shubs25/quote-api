from random import choice

import fastapi
from fastapi import FastAPI, HTTPException, status, Query
from starlette.staticfiles import StaticFiles, FileResponse

import constants
from quote_service import ask_llm

from pathlib import Path

from job_service import create_quote_job

import redis

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

@app.get("/submit-subject", status_code=status.HTTP_202_ACCEPTED)
def submit_subject(subject: str = Query(default=None, min_length=1, max_length=100)):
    if not subject:
        subject = choice(constants.RANDOM_SUBJECT_LIST)

    subject = subject.strip().lower()

    try:
        job_id = create_quote_job(subject)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Quote generation is temporarily unavailable"
        )
    return {
        "subject": subject,
        "job_id": job_id,
        "status": "pending",
    }

@app.get("/quote-jobs/{job_id}", status_code=status.HTTP_200_OK)
def quote_job(job_id: str = fastapi.param_functions.Path(min_length=1, max_length=100)):
    job_id = job_id.strip().lower()
    if not job_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A Job ID must be provided"
        )

    with redis.Redis(host='localhost', port=6379, decode_responses=True) as redis_client:
        try:
            job_status = redis_client.hget(f"quote_job:{job_id}", "status")
            if not job_status:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"A job with Job ID {job_id} does not exist"
                )
            elif job_status == "pending":
                return {
                    "job_id": job_id,
                    "status": job_status,
                    "message": "Your quote is being generated"
                }
            return redis_client.hgetall(f"quote_job:{job_id}")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Quote generation is temporarily unavailable"
            )


@app.get("/quote")
@app.get("/")
@app.get("/ui")
def quote():
    return FileResponse(BASE_DIR / "static" / "index.htm")

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


