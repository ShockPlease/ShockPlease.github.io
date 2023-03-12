import os
import requests
import base64

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

length = 6

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
        os.remove(file)
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

def loop():
    count_no_change = 0  # counter for the number of times the price count has not changed
    while True:
        avgPrices = driver.find_elements(By.CSS_SELECTOR, "span.price-main")
        basePrices = driver.find_elements(By.CSS_SELECTOR, "div.alt")
        names = driver.find_elements(By.CSS_SELECTOR, "span.name")
        if updated(previous=previous): 
            current = len(names)
            if current > previous:
                previous = current
                print(f"Current progress: {current} items loaded. Previous was: {previous - 20}")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                count_no_change = 0
                break
        else:
            count_no_change += 1
            if count_no_change == 25: 
                print("No more new prices.") # this is to prevent the script from running forever
                break
    print("Writing to json...")
    write(basePrices, avgPrices, names)
    print("Done!")
    
def git():
    # specify the owner, repo, and path of the file you want to update
    owner = 'ShockPlease'
    repo = 'ShockPlease.github.io'
    path = 'html/api/api.html'

    # set up the Github API endpoint and retrieve the access token from a repository secret
    api_endpoint = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    access_token = os.environ.get("MY_TOKEN")
    print(access_token)

    # make the API request to get the current content of the file
    response = requests.get(api_endpoint.format(owner=owner, repo=repo, path=path), headers={'Authorization': 'Token ' + access_token})
    response_json = response.json()

    # get the current SHA of the file, which is needed to make the update
    file_sha = response_json['sha']

    loop()
    new_content = open('data/data.json', 'r').read()
    new_content_base64 = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

    # make the API request to update the file
    data = {
        'message': 'Update file',
        'content': new_content_base64,
        'sha': file_sha
    }
    response = requests.put(api_endpoint.format(owner=owner, repo=repo, path=path), json=data, headers={'Authorization': 'Token ' + access_token})

    # print the response status code to make sure the update was successful
    print(response.status_code)

while True:
    loop()
    git()
    time.sleep(3600)
