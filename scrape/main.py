from fastapi import FastAPI
from scraper import scraper

app=FastAPI()
posts=scraper()

@app.get("/scrape")
async def read_item(url:str,num:str):
    return posts.scrapedata(url,num)
