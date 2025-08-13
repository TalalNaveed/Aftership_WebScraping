import asyncio
from crawl4ai import AsyncWebCrawler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time 
import json

options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")

options.add_experimental_option("excludeSwitches", ["enable-automation"])

options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get("https://www.aftership.com/brands/chic.ae?as_source=ecommerce.aftership.com%2Fbrands%2Fpage%2F5")
time.sleep(40)

sidebar_benchmrk = driver.find_element(By.ID, "sidebar-benchmark")
sidebar_information = driver.find_element(By.ID, "sidebar-information")
sidebar_social_media = driver.find_element(By.ID, "sidebar-social-media")

info_blocks = sidebar_information.find_elements(By.CLASS_NAME, "rt-r-gap-1")
info_dict = {}

for block in info_blocks:
    try:
        key_elem = block.find_element(By.CLASS_NAME, "rt-r-weight-medium")
        value_elem = block.find_element(By.CLASS_NAME, "rt-r-size-3")
        key = key_elem.text.strip()
        value = value_elem.text.strip()
        info_dict[key] = value
    except:
        continue  

print(json.dumps(info_dict, indent=2))