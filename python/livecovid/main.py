from fastapi import FastAPI
from scraper import CovidScraper

app = FastAPI(__name__)
covscrape = CovidScraper()

@app.get('/numbers/{state}')
async def get_numbers(state):
    return covscrape.get_covid_numbers(state)