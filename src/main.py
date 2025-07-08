# main.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import logging
from config import CHROMEDRIVER_PATH, START_URL, COOKIES_PATH, DOWNLOAD_FOLDER
from selenium_helper import load_cookies

logging.basicConfig(filename="logs/download_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

def start_download():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.google.com")  # Откройте страницу для загрузки куков
    time.sleep(2)

    load_cookies(driver, COOKIES_PATH)
    driver.get(START_URL)

    # Добавьте здесь логику для скачивания файлов
    # Пример для поиска кнопки "Скачать Word" и клика по ней
    # download_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Download Word')]")
    # download_button.click()

    driver.quit()

if __name__ == "__main__":
    start_download()
