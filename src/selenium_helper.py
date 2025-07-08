# selenium_helper.py
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import json

# Загрузка куков в браузер
def load_cookies(driver: WebDriver, cookie_path: str):
    with open(cookie_path, "r") as file:
        cookies = json.load(file)  # Прочитайте куки в формате JSON
        for cookie in cookies:
            driver.add_cookie(cookie)

# Прочие функции для взаимодействия с Selenium можно добавлять сюда
