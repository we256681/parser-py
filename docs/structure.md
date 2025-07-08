Чтобы указать страницу для парсинга в интерфейсе, нужно добавить в программу поле ввода URL, где пользователь может ввести ссылку на страницу, с которой нужно будет парсить данные.

Вот обновленный пример программы с добавлением поля для ввода URL:

### Обновленный код:

```python
import time
import logging
import os
from tkinter import Tk, filedialog, Button, Label, messagebox, Entry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import json

# Настройка логирования
logging.basicConfig(filename="download_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

# Параметры
cookie_path = ""  # Путь к кукам
start_url = ""  # URL для перехода
download_folder = ""  # Папка для скачивания файлов

# Функция для загрузки куков
def load_cookies(driver, cookie_path):
    with open(cookie_path, "r") as file:
        cookies = json.load(file)  # Прочитайте куки в формате JSON
        for cookie in cookies:
            driver.add_cookie(cookie)

# Функция для работы с Selenium
def start_download():
    global start_url, cookie_path, download_folder

    if not start_url or not cookie_path or not download_folder:
        messagebox.showerror("Ошибка", "Пожалуйста, укажите URL страницы, файл куков и папку для скачивания.")
        return

    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Если не хотите видеть браузер
    chrome_options.add_argument("--disable-gpu")  # Отключение графического интерфейса

    service = Service(executable_path="/path/to/chromedriver")  # Укажите путь до chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Загружаем сайт
    driver.get("https://www.google.com")  # Откройте страницу
    time.sleep(2)
    load_cookies(driver, cookie_path)
    driver.get(start_url)

    # Скачивание файлов
    links = driver.find_elements(By.TAG_NAME, "a")
    download_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and "download" in link.get_attribute("href")]
    
    if not download_links:
        messagebox.showinfo("Информация", "Ссылки для скачивания не найдены.")
        driver.quit()
        return

    downloaded_files = []
    for link in download_links:
        driver.get(link)
        time.sleep(2)
        
        try:
            download_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Download Word')]")  # Пример XPath
            ActionChains(driver).move_to_element(download_button).click().perform()
            time.sleep(3)  # Ждем, пока файл скачивается

            downloaded_files.append(link)
            logging.info(f"Downloaded: {link}")
        except Exception as e:
            logging.error(f"Error while downloading from {link}: {e}")

    driver.quit()

    # Выводим результаты
    messagebox.showinfo("Завершено", f"Файлы скачаны: {len(downloaded_files)}")
    for file in downloaded_files:
        print(f"Downloaded file: {file}")
        logging.info(f"Downloaded file: {file}")

# Функция для выбора файла куков
def choose_cookie_file():
    global cookie_path
    cookie_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if cookie_path:
        label_cookie.config(text=f"Выбран файл: {cookie_path}")

# Функция для выбора папки для скачивания
def choose_download_folder():
    global download_folder
    download_folder = filedialog.askdirectory()
    if download_folder:
        label_folder.config(text=f"Выбрана папка: {download_folder}")

# Функция для получения URL
def set_url():
    global start_url
    start_url = entry_url.get()
    if start_url:
        label_url.config(text=f"URL страницы: {start_url}")

# Создаем графический интерфейс
root = Tk()
root.title("Скачивание файлов с куками")

# Интерфейс
label_url = Label(root, text="Введите URL страницы для парсинга")
label_url.pack(pady=5)

entry_url = Entry(root, width=50)
entry_url.pack(pady=5)

button_set_url = Button(root, text="Установить URL", command=set_url)
button_set_url.pack(pady=5)

label_cookie = Label(root, text="Выберите файл с куками")
label_cookie.pack(pady=5)

button_cookie = Button(root, text="Выбрать файл куков", command=choose_cookie_file)
button_cookie.pack(pady=5)

label_folder = Label(root, text="Выберите папку для скачивания")
label_folder.pack(pady=5)

button_folder = Button(root, text="Выбрать папку", command=choose_download_folder)
button_folder.pack(pady=5)

button_start = Button(root, text="Начать скачивание", command=start_download)
button_start.pack(pady=20)

root.mainloop()
```

### Объяснение изменений:

1. **Поле для ввода URL**:

   * В интерфейсе теперь есть поле для ввода URL страницы, которую нужно будет парсить. Это поле добавлено с помощью `Entry` (ввод текста).

2. **Кнопка для установки URL**:

   * Кнопка "Установить URL" позволяет сохранить введенный URL в глобальную переменную `start_url`, чтобы использовать его при переходе на страницу в Selenium.

3. **Дополнительные проверки**:

   * Программа теперь проверяет, что все параметры (URL, файл куков, папка для скачивания) указаны перед тем, как начать выполнение задачи. Если что-то не указано, появляется сообщение об ошибке.

### Шаги работы с обновленной программой:

1. Введите URL страницы для парсинга в поле ввода.
2. Выберите файл куков, чтобы использовать нужную сессию.
3. Выберите папку для сохранения скачанных файлов.
4. Нажмите "Начать скачивание", чтобы выполнить задачу.

Теперь программа имеет графический интерфейс, который позволяет гибко указывать все необходимые параметры перед началом парсинга и скачивания файлов.
