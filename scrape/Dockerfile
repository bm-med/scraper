FROM python:3.9.0

RUN pip install selenium beautifulsoup4 fastapi uvicorn pymongo

COPY ./SCRAPE /app

WORKDIR /app
CMD [ "uvicorn","app.main:app", "--host","0.0.0.0","--reload"]



