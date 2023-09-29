import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Scraper():
    def __init__(self):
        self.XPATH = '/html/body/div/main/div/div/div[1]/div[2]/a/'

    async def scrapeInfo(self, ctx, query):        
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.get('https://songbpm.com/')
        await ctx.send("Scraping from the Internet...")
        
        elem = driver.find_element(By.NAME, 'query')
        elem.send_keys(query)
        elem.send_keys(Keys.ENTER)
        await ctx.send("Searching from query...")

        try:
            WebDriverWait(driver, 10).until(EC.url_contains("searches"))
            
            title = driver.find_element(By.XPATH, self.XPATH + 'div[1]/div[2]/p[2]').text
            artist = driver.find_element(By.XPATH, self.XPATH + 'div[1]/div[2]/p[1]').text
            key = driver.find_element(By.XPATH, self.XPATH + 'div[2]/div[1]/span[2]').text
            bpm = driver.find_element(By.XPATH, self.XPATH + 'div[2]/div[3]/span[2]').text
            duration = driver.find_element(By.XPATH, self.XPATH + 'div[2]/div[2]/span[2]').text

            result = [title, artist, key, bpm, duration]
            await ctx.send("Elements fetched...")
            driver.close()
            return result

        except Exception as e:
            logging.info(e)
            driver.close()
            return None
