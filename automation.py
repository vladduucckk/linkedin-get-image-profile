from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import requests

from dotenv import load_dotenv

if os.path.isdir(f"{os.getcwd()}/img-profile") is False:
    os.system('mkdir img-profile')

load_dotenv()

LOGIN_LINKEDIN = os.getenv('LOGIN_LINKEDIN')
PASSWORD_LINKEDIN = os.getenv('PASSWORD_LINKEDIN')

url = 'https://www.linkedin.com/login/ru?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url)

login_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')
button_click = driver.find_element(By.XPATH, '//button[@type="submit"]')

login_field.send_keys(LOGIN_LINKEDIN)
password_field.send_keys(PASSWORD_LINKEDIN)
button_click.click()

tab_with_img = driver.current_window_handle
driver.switch_to.window(tab_with_img)
img_profile_src = driver.find_element(By.XPATH, '//a[@class="ember-view block"]//img').get_attribute('src')
response = requests.get(img_profile_src)

with open('img-profile/profile_image.png', 'wb') as f:
    f.write(response.content)
