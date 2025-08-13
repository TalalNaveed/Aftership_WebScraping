import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

df = pd.read_csv("companies_data.csv").head(3)
df.columns = df.columns.str.strip()  
company_links = df["link_for_details"]
company_names = df["company_name"]

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

results = []

for i, (name, url) in enumerate(zip(company_names, company_links)):
    print(f"Scraping ({i+1}/3): {name} - {url}")
    driver.get(url)

    if i == 0:
        print("Solve captcha")
        time.sleep(40)  

    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

    data = {
        "company_name": name.replace("View ", "").replace(" details", ""),
        "url": url,
        "sidebar_info": None,
        "sidebar_benchmark": None,
        "social_media_links": None
    }

    try:
        sidebar_info = driver.find_element(By.ID, "sidebar-information")
        info_blocks = sidebar_info.find_elements(By.CLASS_NAME, "rt-r-gap-1")
        info_dict = {}
        for block in info_blocks:
            try:
                key = block.find_element(By.CLASS_NAME, "rt-r-weight-medium").text.strip()
                value = block.find_element(By.CLASS_NAME, "rt-r-size-3").text.strip()
                info_dict[key] = value
            except:
                continue
        data["sidebar_info"] = json.dumps(info_dict)
    except NoSuchElementException:
        pass

    try:
        sidebar_benchmark = driver.find_element(By.ID, "sidebar-benchmark").text.strip()
        data["sidebar_benchmark"] = sidebar_benchmark
    except NoSuchElementException:
        pass

    try:
        sidebar_social = driver.find_element(By.ID, "sidebar-social-media")
        links = sidebar_social.find_elements(By.TAG_NAME, "a")
        social_links = [
            link.get_attribute("href")
            for link in links
            if link.get_attribute("href") and "linkedin.com" not in link.get_attribute("href")
        ]
        data["social_media_links"] = json.dumps(social_links)
    except NoSuchElementException:
        pass

    results.append(data)

driver.quit()

results_df = pd.DataFrame(results)
results_df.to_csv("phase2_results_demo.csv", index=False)
print("✅ Done. Data saved to 'phase2_results_demo.csv'")
