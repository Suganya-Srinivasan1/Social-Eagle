from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

data = [
      {"name": "Alice Smith", "email": "alice@example.com", "current address": "#12, ABC Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"},
    {"name": "Bob Jones", "email": "bob@example.com", "current address": "#22, XYZ Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"},
    {"name": "Charlie Brown", "email": "charlie@example.com", "current address": "#32, IJK Street, Somecountry", "permanent address":"#12, ABC Street, Somecountry"}
]

# 1. Start the Browser (Chrome)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    for person in data:
        print(f"Filling form for: {person['name']}")
        driver.get("https://demoqa.com/text-box")

        # 2. Wait for the first field to appear
        name_field = wait.until(EC.presence_of_element_located((By.ID, "userName")))
        
        # 3. Enter Data
        name_field.send_keys(person['name'])
        driver.find_element(By.ID, "userEmail").send_keys(person['email'])
        driver.find_element(By.ID, "currentAddress").send_keys(person['current address'])
        driver.find_element(By.ID, "permanentAddress").send_keys(person['permanent address']) 
        # 4. Scroll to and Click Submit
        submit_button = driver.find_element(By.ID, "submit")
        # We use execute_script to click because DemoQA often has ads blocking the button
        driver.execute_script("arguments[0].click();", submit_button)

        print(f"Successfully submitted {person['name']}!")
        time.sleep(2) # Short pause to see the result

finally:
    print("All tasks finished. Closing browser...")
    driver.quit()