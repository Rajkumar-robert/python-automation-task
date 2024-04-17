import os
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv, dotenv_values

load_dotenv()

win_driver_path = "chromedriver-win64/chromedriver.exe"
linux_driver_path = "chromedriver-linux64/chromedriver"

service = Service(executable_path=win_driver_path)
driver = webdriver.Chrome(service=service)
userEmail = os.getenv("USER_EMAIL")
password = os.getenv("PASSWORD")
search_value = "lambo"

driver.get(os.getenv("SITE_URL"))

try:
    home_login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wcgxB")))
    home_login_button.click()
    

    user_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    user_email.send_keys(userEmail)

    user_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    user_password.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "IUoDf")))
    login_button.click()

    search_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "qoZU7")))
    search_field.send_keys(search_value)
    search_field.send_keys(Keys.ENTER)

    for _ in range(76):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)

    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width / 2, screen_height / 2)

    pyautogui.press('enter')

    download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "h3AWh")))
    download_button.click()

    time.sleep(30)
    driver.quit()

except Exception as e:
    print("An error occurred:", e)
    driver.quit()
