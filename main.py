# main.py
# from ff_scraper import get_logs
from scraper.logscraper import get_logs_from_fritzbox

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "Hello World"}


@app.get("/logs")
async def root():
    log_json = get_logs_from_fritzbox()
    return {"msg": "Hello Logs", "logs": log_json}
