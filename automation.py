from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os

from dotenv import load_dotenv

load_dotenv()

LOGIN_LINKEDIN = os.getenv('LOGIN_LINKEDIN')
PASSWORD_LINKEDIN = os.getenv('PASSWORD_LINKEDIN')


url = 'https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url)

login_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')
button_click = driver.find_element(By.XPATH,'//button[@type="submit"]')

login_field.send_keys(LOGIN_LINKEDIN)
password_field.send_keys(PASSWORD_LINKEDIN)
button_click.click()


