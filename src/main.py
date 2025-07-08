# main.py

import tkinter as tk
from tkinter import messagebox, scrolledtext
from settings_manager import save_settings, load_settings, load_settings_by_name
from config import CHROMEDRIVER_PATH, START_URL, COOKIES_PATH, DOWNLOAD_FOLDER, MAX_WORKERS, FILE_EXTENSIONS, LOGIN, PASSWORD, DELAY, MODE
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import logging
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor

# Настройка логирования для отображения логов в интерфейсе
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

def log_message(message):
    """Функция для вывода сообщения в интерфейс"""
    log_text.insert(tk.END, message + '\n')
    log_text.yview(tk.END)  # Прокручиваем текстовый блок вниз

# Функция для авторизации
def login(driver, login, password):
    try:
        # Пример авторизации через поля ввода (имя пользователя и пароль)
        log_message("Авторизация...")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(login)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)  # Ждем загрузку страницы после авторизации
        log_message("Авторизация прошла успешно.")
    except Exception as e:
        log_message(f"Ошибка при авторизации: {e}")
        messagebox.showerror("Ошибка", "Не удалось авторизоваться.")

# Функция для выхода из аккаунта
def logout(driver):
    try:
        logout_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")  # XPath для кнопки выхода
        ActionChains(driver).move_to_element(logout_button).click().perform()
        time.sleep(2)  # Ждем, пока выйдем из аккаунта
        log_message("Выход из аккаунта выполнен.")
    except Exception as e:
        log_message(f"Ошибка при выходе из аккаунта: {e}")

# Функция для авторизации, если куки не действуют
def check_and_login(driver, login, password):
    # Попробуем пройти по страницам, если запросит пароль - авторизуемся
    try:
        log_message(f"Пытаемся зайти на страницу: {START_URL}")
        driver.get(START_URL)
        time.sleep(2)
        
        # Проверим, нужно ли вводить пароль (например, если на странице есть поле ввода пароля)
        if driver.current_url != START_URL:  # Страница изменилась, значит, требуются данные
            login(driver, login, password)
            driver.get(START_URL)  # Перезагружаем страницу
        else:
            log_message("Куки успешно использованы, авторизация не требуется.")
    except Exception as e:
        log_message(f"Ошибка при проверке авторизации: {e}")
        messagebox.showerror("Ошибка", "Не удалось авторизоваться.")

# Функция для сохранения новых настроек
def save_new_settings():
    chromedriver_path = entry_chromedriver_path.get()
    start_url = entry_start_url.get()
    cookies_path = entry_cookies_path.get()
    download_folder = entry_download_folder.get()
    max_workers = int(entry_max_workers.get())
    file_extensions = entry_file_extensions.get().split(',')
    login = entry_login.get()
    password = entry_password.get()
    delay = int(entry_delay.get())
    mode = var_mode.get()

    if chromedriver_path and start_url and cookies_path and download_folder and max_workers and file_extensions and login and password:
        save_settings(
            chromedriver_path,
            start_url,
            cookies_path,
            download_folder,
            max_workers,
            file_extensions,
            login,
            password,
            delay,
            mode
        )
        log_message("Настройки успешно сохранены.")
        update_settings_listbox()  # Обновление списка настроек после сохранения
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

# Загрузка сохранённых настроек
def load_current_settings():
    settings = load_settings()
    
    # Если настройки существуют, используем первую настройку из списка
    if settings:
        current_settings = settings[0]  # Берем первую настройку из списка
    else:
        current_settings = {}
    
    entry_chromedriver_path.delete(0, tk.END)
    entry_chromedriver_path.insert(0, current_settings.get("CHROMEDRIVER_PATH", "path/to/chromedriver"))
    
    entry_start_url.delete(0, tk.END)
    entry_start_url.insert(0, current_settings.get("START_URL", "http://example.com"))
    
    entry_cookies_path.delete(0, tk.END)
    entry_cookies_path.insert(0, current_settings.get("COOKIES_PATH", "cookies/cookies.json"))
    
    entry_download_folder.delete(0, tk.END)
    entry_download_folder.insert(0, current_settings.get("DOWNLOAD_FOLDER", "downloads"))
    
    entry_max_workers.delete(0, tk.END)
    entry_max_workers.insert(0, current_settings.get("MAX_WORKERS", 4))
    
    entry_file_extensions.delete(0, tk.END)
    entry_file_extensions.insert(0, ', '.join(current_settings.get("FILE_EXTENSIONS", ['.docx', '.pdf', '.xlsx'])))
    
    entry_login.delete(0, tk.END)
    entry_login.insert(0, current_settings.get("LOGIN", ""))
    
    entry_password.delete(0, tk.END)
    entry_password.insert(0, current_settings.get("PASSWORD", ""))
    
    entry_delay.delete(0, tk.END)
    entry_delay.insert(0, current_settings.get("DELAY", 2))
    
    var_mode.set(current_settings.get("MODE", "sequential"))

# Функция для обновления списка настроек в интерфейсе
def update_settings_listbox():
    settings = load_settings()
    settings_listbox.delete(0, tk.END)  # Очистка списка перед добавлением новых
    for setting in settings:
        settings_listbox.insert(tk.END, setting.get("LOGIN", "Без логина"))  # Добавление логина в список

# Функция для запуска работы программы
def start_download_task():
    selected_name = settings_listbox.get(tk.ACTIVE)
    
    if selected_name:
        settings = load_settings_by_name(selected_name)
        if settings:
            log_message(f"Загружены настройки: {selected_name}")
            try:
                # Настройка браузера
                chrome_options = Options()
                
                # Проверяем, выбран ли режим "headless" (фоновый режим)
                if var_browser_mode.get() == "headless":
                    chrome_options.add_argument("--headless")  # Без графического интерфейса
                    log_message("Запуск браузера в фоновом режиме.")
                else:
                    log_message("Запуск браузера с графическим интерфейсом.")
                
                service = Service(CHROMEDRIVER_PATH)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Авторизация
                check_and_login(driver, settings['LOGIN'], settings['PASSWORD'])
                
                # Пример выполнения задачи (переходы по ссылкам)
                for i in range(5):  # Пример переходов
                    driver.get(f"{START_URL}/page{i}")
                    log_message(f"Перешли на страницу {START_URL}/page{i}")
                    time.sleep(DELAY)
                
                # Завершаем работу
                logout(driver)
                driver.quit()
            except Exception as e:
                log_message(f"Ошибка при запуске работы: {e}")
                messagebox.showerror("Ошибка", f"Не удалось запустить работу: {e}")
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить настройки.")
    else:
        messagebox.showerror("Ошибка", "Выберите настройки из списка.")

# Главный интерфейс
root = tk.Tk()
root.title("Настройки скачивания файлов")

# Добавление текстового блока для логов
log_text = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
log_text.pack(pady=10)

# Форма для редактирования всех настроек
label_chromedriver_path = tk.Label(root, text="Путь к chromedriver:")
label_chromedriver_path.pack(pady=5)

entry_chromedriver_path = tk.Entry(root)
entry_chromedriver_path.pack(pady=5)

label_start_url = tk.Label(root, text="URL страницы для парсинга:")
label_start_url.pack(pady=5)

entry_start_url = tk.Entry(root)
entry_start_url.pack(pady=5)

label_cookies_path = tk.Label(root, text="Путь к файлу с куками:")
label_cookies_path.pack(pady=5)

entry_cookies_path = tk.Entry(root)
entry_cookies_path.pack(pady=5)

label_download_folder = tk.Label(root, text="Папка для скачивания файлов:")
label_download_folder.pack(pady=5)

entry_download_folder = tk.Entry(root)
entry_download_folder.pack(pady=5)

label_max_workers = tk.Label(root, text="Максимальное количество потоков:")
label_max_workers.pack(pady=5)

entry_max_workers = tk.Entry(root)
entry_max_workers.pack(pady=5)

label_file_extensions = tk.Label(root, text="Расширения файлов для скачивания (через запятую):")
label_file_extensions.pack(pady=5)

entry_file_extensions = tk.Entry(root)
entry_file_extensions.pack(pady=5)

label_login = tk.Label(root, text="Логин:")
label_login.pack(pady=5)

entry_login = tk.Entry(root)
entry_login.pack(pady=5)

label_password = tk.Label(root, text="Пароль:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

label_delay = tk.Label(root, text="Задержка между переходами (в секундах):")
label_delay.pack(pady=5)

entry_delay = tk.Entry(root)
entry_delay.pack(pady=5)

label_mode = tk.Label(root, text="Режим работы:")
label_mode.pack(pady=5)

var_mode = tk.StringVar(value="sequential")
radio_sequential = tk.Radiobutton(root, text="Последовательно", variable=var_mode, value="sequential")
radio_parallel = tk.Radiobutton(root, text="Параллельно", variable=var_mode, value="parallel")
radio_sequential.pack(pady=5)
radio_parallel.pack(pady=5)

label_browser_mode = tk.Label(root, text="Режим браузера:")
label_browser_mode.pack(pady=5)

var_browser_mode = tk.StringVar(value="headless")
radio_headless = tk.Radiobutton(root, text="Без интерфейса", variable=var_browser_mode, value="headless")
radio_display = tk.Radiobutton(root, text="С интерфейсом", variable=var_browser_mode, value="display")
radio_headless.pack(pady=5)
radio_display.pack(pady=5)

button_save_settings = tk.Button(root, text="Сохранить настройки", command=save_new_settings)
button_save_settings.pack(pady=10)

# Список сохранённых настроек
settings_listbox = tk.Listbox(root, height=5)
settings_listbox.pack(pady=5)

# Кнопка для запуска работы
button_start = tk.Button(root, text="Запустить работу", command=start_download_task)
button_start.pack(pady=10)

# Загрузка сохранённых настроек при старте
load_current_settings()

# Обновление списка сохранённых настроек
update_settings_listbox()

root.mainloop()
# Закрытие программы
logging.shutdown()
log_message("Программа завершена.")
messagebox.showinfo("Завершение", "Программа завершена. Логи сохранены в текстовом блоке.")
root.destroy()
# Сохранение логов в файл
with open("logs.txt", "w") as log_file:
    log_file.write(log_text.get("1.0", tk.END))  # Сохраняем весь текст из текстового блока
log_message("Логи сохранены в файл logs.txt.")
