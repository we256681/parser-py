# settings_manager.py
import json
import os

SETTINGS_FILE = "settings.json"

# Функция для сохранения настроек в JSON файл
def save_settings(chromedriver_path, start_url, cookies_path, download_folder, max_workers, file_extensions, login, password, delay, mode):
    settings = {
        "CHROMEDRIVER_PATH": chromedriver_path,
        "START_URL": start_url,
        "COOKIES_PATH": cookies_path,
        "DOWNLOAD_FOLDER": download_folder,
        "MAX_WORKERS": max_workers,
        "FILE_EXTENSIONS": file_extensions,
        "LOGIN": login,
        "PASSWORD": password,
        "DELAY": delay,
        "MODE": mode
    }

    # Проверка, существует ли файл, если нет, создаём его как пустой список
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump([], f)  # Создаем файл как список, если его нет
    
    with open(SETTINGS_FILE, 'r+') as f:
        data = json.load(f)
        
        # Убедимся, что данные это список
        if not isinstance(data, list):
            data = []
        
        # Добавляем новую настройку в список
        data.append(settings)
        
        f.seek(0)  # Перемещаем указатель в начало файла
        json.dump(data, f, indent=4)

# Функция для загрузки всех сохранённых настроек
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return []
    
    with open(SETTINGS_FILE, 'r') as f:
        settings = json.load(f)
    
    # Убедимся, что данные — это список
    if not isinstance(settings, list):
        settings = []
    
    return settings

# Функция для загрузки конкретной настройки по имени
def load_settings_by_name(name):
    settings = load_settings()
    for setting in settings:
        if setting.get("LOGIN") == name:  # Используем логин для поиска
            return setting
    return None
