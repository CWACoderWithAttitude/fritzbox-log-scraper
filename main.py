# main.py
from ff_scraper import get_logs


from fastapi import FastAPI

app = FastAPI()

logs = get_logs()

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.get("/logs")
async def root():
    return {"msg": "Hello Logs"}