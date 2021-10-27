from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# other necessary ones
import urllib.request
import pandas as pd
import json
import time
import re
import datetime
from datetime import date
from scroll import openSeeMore,OpenMoreComments

import pymongo
from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")

db = conn.scraping
collection=db.scraped_data
post = {
        "text":"Mr.Geek",
        "reacts":24,
        "number_of_comments":"delhi",
        "shares":"delhi",
        "dates":"delhi",
        "comments": [
                {"type": "text", "content": "my content"},
                {"type": "image", "content": "my_content"},
                {"type": "image", "content": "my_content"}]
        }
for i in range(0,20):
    







