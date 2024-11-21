import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

db_name = "libraries_data.db"
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS libraries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT,
    city TEXT,
    library TEXT,
    address TEXT,
    zip TEXT,
    phone TEXT
)
''')
service = Service(executable_path="chromedriver.exe") 
driver = webdriver.Chrome(service=service)
driver.maximize_window()

ur = "https://publiclibraries.com/state/"
driver.get(ur)

states = driver.find_elements(By.CSS_SELECTOR, "a[href*='/state/']")
state_links = [state.get_attribute("href") for state in states]

for state_link in state_links:
    driver.get(state_link)
    state_name = driver.find_element(By.TAG_NAME, "h1").text.replace(" Public Libraries", "")
    print(f"Scraping data for {state_name}...")
    rows = driver.find_elements(By.CSS_SELECTOR, "#libraries tbody tr")
    
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) == 5:  
            city = columns[0].text
            library = columns[1].text
            address = columns[2].text
            zip_code = columns[3].text
            phone = columns[4].text



            
            cursor.execute('''
                INSERT INTO libraries (state, city, library, address, zip, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (state_name, city, library, address, zip_code, phone))
    
    connection.commit() 
    time.sleep(2) 

driver.quit()
connection.close()
#print(f"Data sved to{db_name}")
