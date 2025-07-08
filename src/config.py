# config.py (будет использоваться для загрузки настроек)

import json
import os

# Путь к файлу настроек
SETTINGS_FILE = "settings.json"

# Функция для загрузки настроек из файла
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Функция для сохранения настроек в файл
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file, indent=4)

# Загрузка настроек по умолчанию
settings = load_settings()

# Если настройки пустые, используем значения по умолчанию
CHROMEDRIVER_PATH = settings.get("CHROMEDRIVER_PATH", "path/to/chromedriver")
START_URL = settings.get("START_URL", "http://example.com")
COOKIES_PATH = settings.get("COOKIES_PATH", "cookies/cookies.json")
DOWNLOAD_FOLDER = settings.get("DOWNLOAD_FOLDER", "downloads")
MAX_WORKERS = settings.get("MAX_WORKERS", 4)
FILE_EXTENSIONS = settings.get("FILE_EXTENSIONS", ['.docx', '.pdf', '.xlsx'])
