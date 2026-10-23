
from fastapi.testclient import TestClient

import constants
import main

client = TestClient(main.app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_quote_with_subject(monkeypatch):
    monkeypatch.setattr(
        main, "ask_llm", lambda subject: "Courage begins with one step."
    )

    response = client.get("/quote?subject=courage")

    assert response.status_code == 200
    assert response.json() == {
        "subject": "courage",
        "quote": "Courage begins with one step.",
    }


def test_quote_normalizes_subject(monkeypatch):
    monkeypatch.setattr(
        main, "ask_llm", lambda subject: f"A quote about {subject}."
    )

    response = client.get("/quote?subject=Courage")

    assert response.status_code == 200
    assert response.json()["subject"] == "courage"
    assert response.json()["quote"] == "A quote about courage."


def test_quote_without_subject(monkeypatch):
    monkeypatch.setattr(
        main, "ask_llm", lambda subject: f"A quote about {subject}."
    )

    response = client.get("/quote")

    assert response.status_code == 200
    assert response.json()["subject"].upper() in constants.RANDOM_SUBJECT_LIST


def test_quote_generation_failure_returns_503(monkeypatch):
    monkeypatch.setattr(main, "ask_llm", lambda subject: None)

    response = client.get("/quote?subject=courage")

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Quote generation is temporarily unavailable"
    )


def test_empty_subject_returns_422():
    response = client.get("/quote?subject=")

    assert response.status_code == 422
