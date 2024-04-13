from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
userEmail = "rdjrob429+unsplash@gmail.com"
password = "test@123"
search_value="lambo"

driver.get("https://unsplash.com")

home_login_button=driver.find_element(By.CLASS_NAME,"wcgxB")
home_login_button.click()

time.sleep(2)
user_email=driver.find_element(By.CLASS_NAME,"ffHip")
user_email.send_keys(userEmail)

time.sleep(1)
user_password = driver.find_element(By.NAME,"password")
user_password.send_keys(password)

login_button=driver.find_element(By.CLASS_NAME,"IUoDf")
login_button.click()

time.sleep(2)
search_field = driver.find_element(By.CLASS_NAME,"qoZU7")
search_field.send_keys(search_value)
search_field.send_keys(Keys.ENTER)

time.sleep(3)


for _ in range(60):

    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.TAB)

screen_width, screen_height = pyautogui.size()
pyautogui.click(screen_width / 2, screen_height / 2)

time.sleep(1)

pyautogui.press('enter')


download_button=driver.find_element(By.CLASS_NAME,"h3AWh")
download_button.click()

time.sleep(30)
driver.quit()