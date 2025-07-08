# settings_manager.py
import json
import os

SETTINGS_FILE = "settings.json"

# Функция для сохранения настроек в JSON файл
def save_settings(name, chromedriver_path, start_url, cookies_path, download_folder, max_workers, file_extensions):
    settings = {
        "CHROMEDRIVER_PATH": chromedriver_path,
        "START_URL": start_url,
        "COOKIES_PATH": cookies_path,
        "DOWNLOAD_FOLDER": download_folder,
        "MAX_WORKERS": max_workers,
        "FILE_EXTENSIONS": file_extensions
    }
    
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({}, f)  # Если файл пуст, создаём его как пустой объект
    
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Функция для загрузки всех сохранённых настроек
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.load(f)
    return settings
