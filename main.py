import os
from selenium import webdriver
import json
import requests
import base64
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import string
from github import Github

# Github credentials
GITHUB_TOKEN = os.environ['shock_token2']
REPO_NAME = 'ShockPlease.github.io'
FILE_NAME = 'api.html'
FILE_PATH = f'html/api/{FILE_NAME}'

length = 8

items = []

# generate a random string of uppercase letters and digits
letters_and_digits = string.ascii_uppercase + string.digits
random_string = ''.join(random.choices(letters_and_digits, k=length))

for file in os.listdir('.'):
    if file.endswith('.html'):
        os.remove(file)
        print(f'Removed {file}!')

for file in os.listdir('data'):
    if file.endswith('.json'):
        os.remove(f'data\{file}')
        print("Removed file!")
        
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options)  
driver.get("https://tarkov-market.com/")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="__nuxt"]/div/div/div[2]/div[2]/button""")))   

load_more = driver.find_element(By.XPATH, """//*[@id="__nuxt"]/div/div/div[2]/div[2]/button""")
load_more.click()

avgPrices = driver.find_elements(By.CSS_SELECTOR, "span.price-main")
basePrices = driver.find_elements(By.CSS_SELECTOR, "div.alt")
names = driver.find_elements(By.CSS_SELECTOR, "span.name")

previous = 0

while len(names) == previous:
    names = driver.find_elements(By.CSS_SELECTOR, "span.name")

def updated(previous):
    if previous != len(names):
        return True
    elif previous == len(names):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return False

def write(base, alt, name_list):
    strings = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    alt_prices = [alt_price.text.replace("₽", "") for alt_price in alt]
    base_prices = [base_price.text.replace("₽", "") for base_price in base]
    base_prices = [item.text.replace('\u20bd', '').replace('\n', '').replace(':', '') for item in basePrices if item.text.strip() and not any(char in item.text for char in strings) and ':' not in item.text and '\n' not in item.text]
    names = [name.text for name in name_list]
    data = [{"Name": name, "Base Price": base, "Flea Price": alt} for name, base, alt in zip(names, base_prices, alt_prices)]
    with open("data\data.json", "a") as outfile: 
        if outfile.tell() == 0:  # if file is empty, write opening bracket
            outfile.write('[')
        else:  # if file is not empty, move cursor to end of last object and write comma separator
            outfile.seek(-1, 2)
            outfile.write(',')
        json.dump(data, outfile)
        outfile.write(']')

count_no_change = 0  # counter for the number of times there is no change in the number of items on the webpage

while count_no_change < 10:
    try:
        if updated(previous):
            write(basePrices, avgPrices, names)
            previous = len(names)
            print(f"{previous} items saved!")
            count_no_change = 0 # reset counter if there is an update
        else:
            count_no_change += 1 # increment counter if no update
            print(f"No update. Count: {count_no_change}")
            time.sleep(random.randint(1, 3)) # wait for 1-3 seconds before checking for updates
    except Exception as e:
            print(e)
            driver.quit()
driver.quit()

# Commit changes to Github
g = Github(GITHUB_TOKEN)
repo = g.get_user().get_repo(REPO_NAME)
with open(FILE_PATH, 'rb') as file:
    content = file.read()
    content_base64 = base64.b64encode(content)
try:
    repo.get_contents(FILE_NAME)
    repo.update_file(FILE_NAME, "Updated data.json", content_base64.decode('utf-8'))
    print(f"{FILE_NAME} updated!")
except:
    repo.create_file(FILE_NAME, "Initial commit", content_base64.decode('utf-8'))
    print(f"{FILE_NAME} created!")
