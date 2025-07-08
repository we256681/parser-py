# main.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
from settings_manager import save_settings, load_settings, load_settings_by_name
from config import CHROMEDRIVER_PATH, START_URL, COOKIES_PATH, DOWNLOAD_FOLDER, MAX_WORKERS, FILE_EXTENSIONS, LOGIN, PASSWORD, DELAY, MODE
import chromedriver_binary  # автоматом добавит путь chromedriver в PATH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Попытка импорта chromedriver_binary для автоматического управления драйвером
try:
    import chromedriver_binary
    CHROMEDRIVER_AUTO_INSTALL = True
    print("ChromeDriver будет использован из chromedriver_binary")
except ImportError:
    CHROMEDRIVER_AUTO_INSTALL = False
    print("chromedriver_binary не найден, используется ручной путь")

# Настройка логирования для отображения логов в интерфейсе
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

def log_message(message):
    """Функция для вывода сообщения в интерфейс"""
    if 'log_text' in globals():
        log_text.insert(tk.END, message + '\n')
        log_text.yview(tk.END)  # Прокручиваем текстовый блок вниз
    print(message)  # Дублируем в консоль

def get_chrome_driver():
    """Функция для создания Chrome WebDriver с правильными настройками"""
    chrome_options = Options()
    
    # Проверяем, выбран ли режим "headless" (фоновый режим)
    if 'var_browser_mode' in globals() and var_browser_mode.get() == "headless":
        chrome_options.add_argument("--headless")
        log_message("Запуск браузера в фоновом режиме.")
    else:
        log_message("Запуск браузера с графическим интерфейсом.")
    
    # Дополнительные опции для стабильной работы
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    # Настройки для загрузки файлов
    download_folder = os.path.abspath(DOWNLOAD_FOLDER)
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        if CHROMEDRIVER_AUTO_INSTALL:
            # Используем chromedriver_binary для автоматического управления
            log_message("Используется chromedriver_binary для автоматического управления драйвером")
            driver = webdriver.Chrome(options=chrome_options)
        else:
            # Используем ручной путь к chromedriver
            chromedriver_path = CHROMEDRIVER_PATH
            if not os.path.exists(chromedriver_path):
                log_message(f"ChromeDriver не найден по пути: {chromedriver_path}")
                # Попытаемся найти chromedriver в системе
                import shutil
                system_chromedriver = shutil.which('chromedriver')
                if system_chromedriver:
                    chromedriver_path = system_chromedriver
                    log_message(f"Найден системный chromedriver: {chromedriver_path}")
                else:
                    raise FileNotFoundError("ChromeDriver не найден в системе")
            
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        log_message("ChromeDriver успешно инициализирован")
        return driver
        
    except Exception as e:
        log_message(f"Ошибка при инициализации ChromeDriver: {e}")
        log_message("Попытка использования webdriver-manager...")
        
        try:
            # Попытка использования webdriver-manager как fallback
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message("ChromeDriver успешно инициализирован через webdriver-manager")
            return driver
        except ImportError:
            log_message("webdriver-manager не установлен. Установите его: pip install webdriver-manager")
            raise
        except Exception as e2:
            log_message(f"Ошибка при использовании webdriver-manager: {e2}")
            raise

def load_cookies(driver, cookie_path):
    """Функция для загрузки куков"""
    try:
        if os.path.exists(cookie_path):
            with open(cookie_path, "r") as file:
                cookies = json.load(file)
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except Exception as e:
                        log_message(f"Ошибка при добавлении куки: {e}")
            log_message(f"Куки загружены из файла: {cookie_path}")
        else:
            log_message(f"Файл с куками не найден: {cookie_path}")
    except Exception as e:
        log_message(f"Ошибка при загрузке куков: {e}")

def login(driver, login_text, password_text):
    """Функция для авторизации"""
    try:
        log_message("Попытка авторизации...")
        
        # Ждем загрузки страницы
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Ищем поля для ввода логина и пароля
        username_field = None
        password_field = None
        
        # Различные варианты поиска полей авторизации
        login_selectors = [
            (By.NAME, "username"),
            (By.NAME, "login"),
            (By.NAME, "email"),
            (By.ID, "username"),
            (By.ID, "login"),
            (By.ID, "email"),
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.CSS_SELECTOR, "input[type='email']")
        ]
        
        password_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']")
        ]
        
        # Поиск поля логина
        for selector in login_selectors:
            try:
                username_field = driver.find_element(*selector)
                break
            except:
                continue
        
        # Поиск поля пароля
        for selector in password_selectors:
            try:
                password_field = driver.find_element(*selector)
                break
            except:
                continue
        
        if username_field and password_field:
            username_field.clear()
            username_field.send_keys(login_text)
            password_field.clear()
            password_field.send_keys(password_text)
            password_field.send_keys(Keys.RETURN)
            
            time.sleep(3)  # Ждем загрузку страницы после авторизации
            log_message("Авторизация выполнена успешно")
        else:
            log_message("Поля для авторизации не найдены на странице")
            
    except Exception as e:
        log_message(f"Ошибка при авторизации: {e}")

def check_and_login(driver, login_text, password_text):
    """Функция для проверки и авторизации при необходимости"""
    try:
        log_message(f"Переход на страницу: {START_URL}")
        driver.get(START_URL)
        time.sleep(2)
        
        # Загружаем куки если они есть
        if os.path.exists(COOKIES_PATH):
            load_cookies(driver, COOKIES_PATH)
            driver.refresh()
            time.sleep(2)
        
        # Проверяем, требуется ли авторизация
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        if ("login" in page_source or "password" in page_source or 
            "авторизация" in page_source or "войти" in page_source):
            log_message("Обнаружена страница авторизации")
            login(driver, login_text, password_text)
        else:
            log_message("Авторизация не требуется или уже выполнена")
            
    except Exception as e:
        log_message(f"Ошибка при проверке авторизации: {e}")

def save_new_settings():
    """Функция для сохранения новых настроек"""
    try:
        chromedriver_path = entry_chromedriver_path.get()
        start_url = entry_start_url.get()
        cookies_path = entry_cookies_path.get()
        download_folder = entry_download_folder.get()
        max_workers = int(entry_max_workers.get() or 1)
        file_extensions = [ext.strip() for ext in entry_file_extensions.get().split(',') if ext.strip()]
        login_text = entry_login.get()
        password_text = entry_password.get()
        delay = int(entry_delay.get() or 5)
        mode = var_mode.get()

        if start_url and download_folder and login_text and password_text:
            save_settings(
                chromedriver_path,
                start_url,
                cookies_path,
                download_folder,
                max_workers,
                file_extensions,
                login_text,
                password_text,
                delay,
                mode
            )
            log_message("Настройки успешно сохранены.")
            update_settings_listbox()
        else:
            messagebox.showerror("Ошибка", "Заполните обязательные поля: URL, папка загрузки, логин, пароль!")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка в числовых значениях: {e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при сохранении настроек: {e}")

def load_current_settings():
    """Загрузка текущих настроек в интерфейс"""
    settings = load_settings()
    
    if settings:
        current_settings = settings[0]
    else:
        current_settings = {}
    
    # Очистка и заполнение полей
    fields = [
        (entry_chromedriver_path, "CHROMEDRIVER_PATH", "chromedriver" if CHROMEDRIVER_AUTO_INSTALL else "path/to/chromedriver"),
        (entry_start_url, "START_URL", "http://example.com"),
        (entry_cookies_path, "COOKIES_PATH", "cookies/cookies.json"),
        (entry_download_folder, "DOWNLOAD_FOLDER", "downloads"),
        (entry_max_workers, "MAX_WORKERS", 4),
        (entry_login, "LOGIN", ""),
        (entry_password, "PASSWORD", ""),
        (entry_delay, "DELAY", 2)
    ]
    
    for field, key, default in fields:
        field.delete(0, tk.END)
        field.insert(0, str(current_settings.get(key, default)))
    
    # Обработка расширений файлов
    entry_file_extensions.delete(0, tk.END)
    extensions = current_settings.get("FILE_EXTENSIONS", ['.docx', '.pdf', '.xlsx'])
    entry_file_extensions.insert(0, ', '.join(extensions))
    
    # Режим работы
    var_mode.set(current_settings.get("MODE", "sequential"))

def update_settings_listbox():
    """Обновление списка настроек"""
    settings = load_settings()
    settings_listbox.delete(0, tk.END)
    for i, setting in enumerate(settings):
        display_name = f"{i+1}. {setting.get('LOGIN', 'Без логина')} - {setting.get('START_URL', 'Без URL')[:50]}..."
        settings_listbox.insert(tk.END, display_name)

def start_download_task():
    """Функция для запуска основной задачи"""
    selection = settings_listbox.curselection()
    
    if not selection:
        messagebox.showerror("Ошибка", "Выберите настройки из списка.")
        return
    
    selected_index = selection[0]
    settings = load_settings()
    
    if selected_index >= len(settings):
        messagebox.showerror("Ошибка", "Выбранные настройки не найдены.")
        return
    
    selected_settings = settings[selected_index]
    log_message(f"Загружены настройки: {selected_settings.get('LOGIN', 'Без логина')}")
    
    driver = None
    try:
        # Обновляем глобальные переменные
        global CHROMEDRIVER_PATH, START_URL, COOKIES_PATH, DOWNLOAD_FOLDER, MAX_WORKERS, FILE_EXTENSIONS, LOGIN, PASSWORD, DELAY, MODE
        
        CHROMEDRIVER_PATH = selected_settings.get('CHROMEDRIVER_PATH', CHROMEDRIVER_PATH)
        START_URL = selected_settings.get('START_URL', START_URL)
        COOKIES_PATH = selected_settings.get('COOKIES_PATH', COOKIES_PATH)
        DOWNLOAD_FOLDER = selected_settings.get('DOWNLOAD_FOLDER', DOWNLOAD_FOLDER)
        MAX_WORKERS = selected_settings.get('MAX_WORKERS', MAX_WORKERS)
        FILE_EXTENSIONS = selected_settings.get('FILE_EXTENSIONS', FILE_EXTENSIONS)
        LOGIN = selected_settings.get('LOGIN', LOGIN)
        PASSWORD = selected_settings.get('PASSWORD', PASSWORD)
        DELAY = selected_settings.get('DELAY', DELAY)
        MODE = selected_settings.get('MODE', MODE)
        
        # Создаем папку для загрузки если её нет
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)
        
        # Инициализация драйвера
        driver = get_chrome_driver()
        
        # Авторизация
        check_and_login(driver, LOGIN, PASSWORD)
        
        # Здесь добавьте вашу логику парсинга и скачивания
        log_message("Начинаем парсинг страницы...")
        
        # Пример базового парсинга
        links = driver.find_elements(By.TAG_NAME, "a")
        log_message(f"Найдено {len(links)} ссылок на странице")
        
        # Фильтруем ссылки по расширениям файлов
        download_links = []
        for link in links:
            href = link.get_attribute("href")
            if href and any(ext in href.lower() for ext in FILE_EXTENSIONS):
                download_links.append(href)
        
        log_message(f"Найдено {len(download_links)} ссылок для скачивания")
        
        # Здесь можно добавить логику скачивания файлов
        for i, link in enumerate(download_links[:5]):  # Ограничиваем для примера
            log_message(f"Обрабатываем ссылку {i+1}/{len(download_links)}: {link}")
            time.sleep(DELAY)
        
        log_message("Задача выполнена успешно!")
        
    except Exception as e:
        log_message(f"Ошибка при выполнении задачи: {e}")
        messagebox.showerror("Ошибка", f"Не удалось выполнить задачу: {e}")
    
    finally:
        if driver:
            try:
                driver.quit()
                log_message("Браузер закрыт")
            except:
                pass

# Создание главного окна
root = tk.Tk()
root.title("Настройки скачивания файлов")
root.geometry("800x900")

# Текстовый блок для логов
log_frame = tk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

log_label = tk.Label(log_frame, text="Логи выполнения:")
log_label.pack(anchor=tk.W)

log_text = scrolledtext.ScrolledText(log_frame, width=80, height=10, wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, expand=True)

# Форма настроек
settings_frame = tk.Frame(root)
settings_frame.pack(fill=tk.X, padx=10, pady=5)

# Создание полей ввода
fields = [
    ("Путь к chromedriver:", "entry_chromedriver_path"),
    ("URL страницы для парсинга:", "entry_start_url"),
    ("Путь к файлу с куками:", "entry_cookies_path"),
    ("Папка для скачивания файлов:", "entry_download_folder"),
    ("Максимальное количество потоков:", "entry_max_workers"),
    ("Расширения файлов (через запятую):", "entry_file_extensions"),
    ("Логин:", "entry_login"),
    ("Пароль:", "entry_password"),
    ("Задержка между переходами (сек):", "entry_delay")
]

for label_text, entry_name in fields:
    label = tk.Label(settings_frame, text=label_text)
    label.pack(anchor=tk.W, pady=(5, 0))
    
    if entry_name == "entry_password":
        entry = tk.Entry(settings_frame, show="*", width=60)
    else:
        entry = tk.Entry(settings_frame, width=60)
    
    entry.pack(fill=tk.X, pady=(0, 5))
    globals()[entry_name] = entry

# Режим работы
mode_frame = tk.Frame(settings_frame)
mode_frame.pack(fill=tk.X, pady=5)

tk.Label(mode_frame, text="Режим работы:").pack(anchor=tk.W)
var_mode = tk.StringVar(value="sequential")
tk.Radiobutton(mode_frame, text="Последовательно", variable=var_mode, value="sequential").pack(anchor=tk.W)
tk.Radiobutton(mode_frame, text="Параллельно", variable=var_mode, value="parallel").pack(anchor=tk.W)

# Режим браузера
browser_frame = tk.Frame(settings_frame)
browser_frame.pack(fill=tk.X, pady=5)

tk.Label(browser_frame, text="Режим браузера:").pack(anchor=tk.W)
var_browser_mode = tk.StringVar(value="headless")
tk.Radiobutton(browser_frame, text="Без интерфейса", variable=var_browser_mode, value="headless").pack(anchor=tk.W)
tk.Radiobutton(browser_frame, text="С интерфейсом", variable=var_browser_mode, value="display").pack(anchor=tk.W)

# Кнопка сохранения настроек
button_save_settings = tk.Button(settings_frame, text="Сохранить настройки", command=save_new_settings)
button_save_settings.pack(pady=10)

# Список сохранённых настроек
list_frame = tk.Frame(root)
list_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(list_frame, text="Сохранённые настройки:").pack(anchor=tk.W)
settings_listbox = tk.Listbox(list_frame, height=5)
settings_listbox.pack(fill=tk.X, pady=5)

# Кнопка запуска
button_start = tk.Button(root, text="Запустить работу", command=start_download_task, bg="green", fg="white")
button_start.pack(pady=10)

# Инициализация
log_message("Программа запущена")
if CHROMEDRIVER_AUTO_INSTALL:
    log_message("Используется автоматическое управление ChromeDriver")
else:
    log_message("Используется ручное управление ChromeDriver")

load_current_settings()
update_settings_listbox()

# Запуск главного цикла
root.mainloop()
