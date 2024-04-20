import os
import pyautogui
import time
from datetime import datetime,timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv, dotenv_values

load_dotenv()
def main():

    win_driver_path = "chromedriver-win64/chromedriver.exe"
    linux_driver_path = "chromedriver-linux64/chromedriver"

    service = Service(executable_path=win_driver_path)
    driver = webdriver.Chrome(service=service)
    userEmail = os.getenv("USER_EMAIL")
    password = os.getenv("PASSWORD")

    # Get current date and time
    current_datetime = datetime.now()

    # Get yesterday's date at the current time
    yesterday_datetime = current_datetime - timedelta(days=1)

    # Format dates as required
    current_date_str = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    yesterday_date_str = yesterday_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    # Modify the URL with the date parameters
    new_url =f"&completedFrom={yesterday_date_str}&completedTo={current_date_str}"

    #testing url to get records
    test_url ="&completedFrom=2024-04-13T19:14:54&completedTo=2024-04-18T19:14:54"
    completion_expired_url="4,"
    driver.get(os.getenv("SITE_URL"))


    try:
        time.sleep(4)
        cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonAccept")))
        cookie_button.click()

        user_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        user_email.send_keys(userEmail)

        user_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        user_password.send_keys(password)

        sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginBtn")))
        sign_in_button.click()

        time.sleep(10)
        completed_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "completed-course")))
        completed_button.click()
    
        # Switch to the newly opened tab
        driver.switch_to.window(driver.window_handles[-1])

        #changing new url
        time.sleep(20)
        pyautogui.press('f6')
        pyautogui.press('home')
        time.sleep(5)
        pyautogui.press('right',presses=130)
        pyautogui.typewrite(completion_expired_url)
        time.sleep(5)
        pyautogui.press('enter')
        time.sleep(25)

        download_options_button= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='align-center-vertical app-avatar ng-star-inserted'])[4]")))
        download_options_button.click()
    
        #selecting document format
        time.sleep(2)
        driver.find_element(By.XPATH,"//div[@class='cdk-overlay-container']/div[2]").click()
        pyautogui.press('down')
        pyautogui.press('enter')

        time.sleep(2)
        download_button =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//mat-dialog-actions[@class='mat-dialog-actions popup-footer ng-star-inserted']/button[2]")))
        download_button.click()
    
        #waiting for download
        time.sleep(10)
        driver.quit()

        

    except Exception as e:
        print("An error occurred:", e)
        driver.quit()

if __name__ == "__main__":
    main()  