import os
from scrapers.covid import CovidScraper
from fastapi import FastAPI
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
covscrape = CovidScraper()


@app.get("/numbers/{state}")
async def get_numbers(state):
    return covscrape.get_covid_numbers(state)


@app.get("/")
async def get_root():
    return FileResponse("app/index.html")


