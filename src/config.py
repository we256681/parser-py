# config.py

import json
import os

SETTINGS_FILE = "settings.json"

# Функция для загрузки настроек из файла
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            return json.load(file)
    return []

# Функция для сохранения настроек в файл
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

# Загрузка настроек из списка (если они есть)
settings = load_settings()

# Если настройки пустые или их нет, используем значения по умолчанию
if settings:
    current_settings = settings[0]  # Если настроек несколько, выбираем первую
else:
    current_settings = {}

CHROMEDRIVER_PATH = current_settings.get("CHROMEDRIVER_PATH", "path/to/chromedriver")
START_URL = current_settings.get("START_URL", "http://example.com")
COOKIES_PATH = current_settings.get("COOKIES_PATH", "cookies/cookies.json")
DOWNLOAD_FOLDER = current_settings.get("DOWNLOAD_FOLDER", "downloads")
MAX_WORKERS = current_settings.get("MAX_WORKERS", 4)
FILE_EXTENSIONS = current_settings.get("FILE_EXTENSIONS", ['.docx', '.pdf', '.xlsx'])
LOGIN = current_settings.get("LOGIN", "")  # Логин для авторизации
PASSWORD = current_settings.get("PASSWORD", "")  # Пароль для авторизации
DELAY = current_settings.get("DELAY", 2)  # Задержка между переходами по ссылкам
MODE = current_settings.get("MODE", "sequential")  # Режим работы: "sequential" или "parallel"
