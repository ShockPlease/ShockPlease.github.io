import os
from selenium import webdriver
import json
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
basePrices = driver.find_elements(By.CLASS_NAME, "alt")
names = driver.find_elements(By.CSS_SELECTOR, "span.name")

previous = 0

while len(names) == previous:
    names = driver.find_elements(By.CSS_SELECTOR, "span.name")

def updated(previous):
    if previous != len(prices):
        return True
    elif previous == len(prices):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return False

def write(base, alt, name_list):
    alt_prices = [alt.text.replace("₽", "") for alt_price in alt]
    base_prices = [base.text.replace("₽", "") for base_price in base]
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

count_no_change = 0  # counter for the number of times the price count has not changed
while True:
    avgPrices = driver.find_elements(By.CSS_SELECTOR, "span.price-main")
    basePrices = driver.find_elements(By.CLASS_NAME, "alt")
    names = driver.find_elements(By.CSS_SELECTOR, "span.name")
    if updated(previous=previous): 
        current = len(names)
        if current > previous:
            previous = current
            print(f"Current progress: {current} items loaded. Previous was: {previous - 20}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            count_no_change = 0
    else:
        count_no_change += 1
        if count_no_change == 25: 
            print("No more new prices.") # this is to prevent the script from running forever
            break

print("Writing to json...")
write(prices, names)
print("Done!")

print("Writing to html...")
try:
    with open('index.html', 'w+') as index_file:
        with open('data/data.json', 'r') as data_file:
            index_file.write(data_file.read())
except Exception as e:
    print(f'An error occurred: {e}')
print("Done!")

driver.quit()
index_file.close()
data_file.close()
