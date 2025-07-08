# selenium_helper.py

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import json
import os

# Загрузка куков в браузер
def load_cookies(driver: WebDriver, cookie_path: str):
    with open(cookie_path, "r") as file:
        cookies = json.load(file)  # Прочитайте куки в формате JSON
        for cookie in cookies:
            driver.add_cookie(cookie)

# Функция для фильтрации ссылок по расширению файлов
def filter_links_by_extension(links, extensions):
    filtered_links = []
    for link in links:
        if any(link.endswith(ext) for ext in extensions):
            filtered_links.append(link)
    return filtered_links

# Пример функции для перехода по ссылкам
def parse_links(driver: WebDriver, extensions):
    links = driver.find_elements(By.TAG_NAME, "a")
    all_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]
    return filter_links_by_extension(all_links, extensions)
