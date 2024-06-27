# main.py
# from ff_scraper import get_logs
from scraper.logscraper import get_logs_from_fritzbox
from fastapi.testclient import TestClient
from typing import Dict
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "Ei Gude!"}


def get_logs() -> Dict:
    logs = get_logs_from_fritzbox()
    return logs


@app.get("/logs")
async def root():
    log_json = get_logs_from_fritzbox()
    return {"msg": "EI Gude!", "logs": log_json}


test_client = TestClient(app)


def test_get_root():
    response = test_client.get("/")
    assert response.status_code == 200
    rj = response.json()
    assert rj == {"msg": "Ei Gude!"}
    assert "msg" in rj.keys()


def test_get_logs():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Ei Gude!"}


def test_get_logs_contains_log_key():
    response = test_client.get("/logs")
    rj = response.json()
    assert "logs" in rj.keys()


# def test_get_logs():
#    respone = test_client.get("/logs")
#    assert respone.status_code == 200
