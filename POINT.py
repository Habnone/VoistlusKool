from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import sqlite3

driver = webdriver.Chrome()

conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,
    url TEXT,
    brand TEXT,
    engine TEXT,
    mileage INTEGER,
    fuel TEXT,
    model TEXT,
    model_short TEXT,
    transmission TEXT,
    year INTEGER,
    bodytype TEXT,
    drive TEXT,
    price INTEGER
)
'''

cursor.execute(create_table_query)
conn.commit()

driver.get("https://www.auto24.ee/soidukid/")
text = driver.page_source
text = BeautifulSoup(text, 'html.parser').get_text()
price_elements = driver.find_elements(By.CSS_SELECTOR, '.price, a')
mlist = []
print(price_elements)
for i in price_elements:
    href = i.get_attribute('href')
    if 'https://www.auto24.ee/soidukid/' in str(href) and len(str(href)) > 32:
        mlist.append(href)

print(mlist)

count = 0

for i in mlist:
    driver.get(i)
    nimi = driver.find_element(By.CSS_SELECTOR, '.commonSubtitle').text
    brand = nimi.split(" ")[0]
    mudel = driver.find_elements(By.CSS_SELECTOR, '.b-breadcrumbs__item')[2].text
    kytus = driver.find_element(By.CSS_SELECTOR, '.field-kytus').text[6:]
    aasta = driver.find_element(By.CSS_SELECTOR, '.field-month_and_year').text[-4:]
    varvus = driver.find_element(By.CSS_SELECTOR, '.field-varvus').text.split(" ")[1]
    vedavsild = driver.find_element(By.CSS_SELECTOR, '.field-vedavsild').text.split(" ")[2]
    labisoit = driver.find_element(By.CSS_SELECTOR, '.field-labisoit').text
    labisoit = re.findall("\d+", labisoit)
    labisoit = "".join(labisoit)
    mootor = driver.find_element(By.CSS_SELECTOR, '.field-mootorvoimsus').text[7:]
    keretyyp = driver.find_element(By.CSS_SELECTOR, '.field-keretyyp').text[9:]
    kast = driver.find_element(By.CSS_SELECTOR, '.field-kaigukast_kaikudega').text
    hind = driver.find_element(By.CSS_SELECTOR, '.field-hind').text
    print(hind)
    car_info = {
    "url": mlist[count],
    "brand": brand,
    "engine": mootor,
    "mileage": labisoit,
    "fuel": kytus,
    "model": mudel,
    "model_short": mudel,
    "transmission": kast,
    "year": aasta,
    "bodytype": keretyyp,
    "drive": vedavsild,
    "price": hind
    }

    insert_query = '''
    INSERT INTO cars (url, brand, engine, mileage, fuel, model, model_short, transmission, year, bodytype, drive, price)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (
        car_info['url'],
        car_info['brand'],
        car_info['engine'],
        car_info['mileage'],
        car_info['fuel'],
        car_info['model'],
        car_info['model_short'],
        car_info['transmission'],
        car_info['year'],
        car_info['bodytype'],
        car_info['drive'],
        car_info['price']
    ))
    conn.commit()


driver.quit()