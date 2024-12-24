import logging
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
from logging import getLogger, basicConfig, INFO
from dotenv import load_dotenv

# настройка конфігу для логера
loger = getLogger()
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
file_handler = logging.FileHandler("out.log")
basicConfig(level=INFO, format=FORMAT, handlers=[file_handler])

# якщо папки не існує вона створиться
if os.path.isdir(f"{os.getcwd()}/img-profile") is False:
    os.system('mkdir img-profile')
    logging.info("Створенно директорію для зберігання зображення")

load_dotenv()

LOGIN_LINKEDIN = os.getenv('LOGIN_LINKEDIN')
PASSWORD_LINKEDIN = os.getenv('PASSWORD_LINKEDIN')
# PROXY = os.getenv('PROXY')

url = 'https://www.linkedin.com/login/'

# створення драйверу для хрому та додавання опцій
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument(f'--proxy-server={PROXY}')
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3")
# використання атрибуту --headless, щоб програма запускалась в фоні(для економії ресурсів)
# chrome_options.add_argument('--headless')
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# перехід на сторінку авторизації Linkedin
driver.get(url)
logging.info("Відкрито браузер")
time.sleep(2)

# отримання веб-елементів для заповнення та відправки на сервер
login_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')
button_click = driver.find_element(By.XPATH, '//button[@type="submit"]')

# заповнення та відправка на сервер
login_field.send_keys(LOGIN_LINKEDIN)
logging.info("Логін заповненно")
time.sleep(2)
password_field.send_keys(PASSWORD_LINKEDIN)
logging.info("Пароль заповненно")
time.sleep(2)
button_click.click()

# якщо url починається з цієї адреси, значить потрібно пройти капчу(у вас є 20 секунд)
if driver.current_url.startswith("https://www.linkedin.com/checkpoint/challenge/"):
    time.sleep(15)

# якщо після авторизації ми не перейшли на головну сторінку, значить дані невірні
if driver.current_url != "https://www.linkedin.com/feed/":
    logging.critical("Невдалось авторизуватися(невірний логін або пароль)")
    logging.info("Браузер закрито")
    raise ValueError("Невірні дані для входу")

logging.info("Авторизовано")
time.sleep(2)

# переключення драйверу на вкладку з зображенням
tab_with_img = driver.current_window_handle
driver.switch_to.window(tab_with_img)

# отримання атрибуту src для зображення
img_profile_src = driver.find_element(By.XPATH, '//a[@class="ember-view block"]//img').get_attribute('src')
response = requests.get(img_profile_src)

# запис зображення до директорії
with open('img-profile/profile_image.png', 'wb') as f:
    f.write(response.content)
    logging.info("Фото завантажилось")
logging.info("Закрито браузер")
