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

class scraper():
    def scrapedata(self,url,num):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)
        #specify the path to chromedriver.exe
        #path='C:/Users/Med/Desktop/cdriver/chromedriver.exe'
        #driver = webdriver.Chrome(path,options=chrome_options)
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s,options=chrome_options)
        with open('facebook_credentials.txt') as file:
            EMAIL = file.readline().split('"')[0]
            PASSWORD = file.readline().split('"')[0]
        #open the webpage
        driver.get("http://www.facebook.com")
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(EMAIL)
        pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(PASSWORD)
        #target the login button and click it
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        time.sleep(10)
        driver.get(url)
        time.sleep(10)

                
        count = 0
        switch = True
        old_numReviews = 0
        specifiedNumber = num # number of reviews to get

        while switch:
            count += 1
            #open comments
            OpenMoreComments(driver)
            #open see more
            openSeeMore(driver)
            # scroll to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            # process check
            reviewList = driver.find_elements_by_xpath("//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']")
            numReviews = len(reviewList)
            if old_numReviews < numReviews:
                print('Scroll Count:', count, '  numReviews:', numReviews)
            old_numReviews = numReviews
            
            # termination condition
            if numReviews >= int(specifiedNumber):
                switch = False
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);") # scroll back to the top
        time.sleep(10)
        source_data = driver.page_source
        bs_data = bs(source_data, 'html.parser')
        reviews = bs_data.find_all('div', {'class':'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'})
        reviews=reviews[0:int(specifiedNumber)]
        reacts = []
        users = []
        usernames = []
        dates = []
        texts = []
        types = []
        links=[]
        num_comments=[]
        shares=[]
        posts=[]
        
        final_list=[]
        for idx,r in enumerate(reviews):
            list_of_comments=[]

            #get the number of reacts on a post
            react = r.find('span',{"class":"pcp91wgn"}).get_text()
            if ('K'in react):
                react=re.sub("\xa0",'',react)
            reacts.append(react)

            #get the link of a post
            try:
                link = r.find('a',{"class":"oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 a8c37x1j p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 p8dawk7l"}).get('href')  
                
            except:
                link='no link'
            links.append(link)

            #get the number of comments
            num_comm = r.find('span',{"class":"d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v b1v8xokw m9osqain"}).get_text()
            num_comments.append(num_comm)

            #get the number of shares
            share = r.find_all('span',{"class":"d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db gfeo3gy3 a3bd9o3v b1v8xokw m9osqain"})
            try:
                shar=share[1].get_text()
            except:
                shar='no shares'
            shares.append(shar)

            #get the text of the post
            text = r.find('div',{'class':['kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q','o9v6fnle cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']}).get_text()
            posts.append(text)

            #get the date of the post
            dat = r.find('a',{'class':'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw'}).get('aria-label')
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            if ('h' in dat):
                dates.append(' '.join(dat.split()[:2])+','+d1) 
            elif (' ' not in dat) and ('j' in dat):
                date1 = d1 - datetime.timedelta(days=int(dat[0]))
                dates.append(date1)
            elif ('2020' in dat) or ('2019' in dat) or ('2018' in dat):
                dates.append(dat)
            else:
                dates.append(' '.join(dat.split()[:2])+','+d1)

            #get the comments of the post
            comments = r.find_all('div',{'class':'l9j0dhe7 ecm0bbzt rz4wbd8a qt6c0cv9 dati1w0a j83agx80 btwxx1t3 lzcic4wl'})
            for comment in comments:
                typ=comment.get('aria-label')
                types.append(comment.get('aria-label'))
                tex = comment.find('div',{"class":"kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"})
                if tex is None:
                    texts.append('no text')
                else:
                    l=tex.get_text().strip()
                    k={"type": typ, "content": l}
                    list_of_comments.append(k)
            final_list.append(list_of_comments)
        #connect to mongodb
        try:
            conn = MongoClient(host='test_mongodb',port=27017,user='root',PASSWORD='pass',authSource='admin')
            print("Connected successfully!!!")
        except:  
            print("Could not connect to MongoDB")

        db = conn['scraping_db']
        collection=db.scraped_data
        #insert posts in our mongodb database
        for i in range(0,int(specifiedNumber)):
            post = {
                "text":posts[i],
                "link":links[i],
                "reacts":reacts[i],
                "number_of_comments":num_comments[i],
                "shares":shares[i],
                "dates":dates[i],
                "comments": final_list[i]
                    
        }
            ps = collection.insert_one(post)
        return ('Page Scraped Successfully !')

        