# main.py

import tkinter as tk
from tkinter import messagebox
from settings_manager import save_settings, load_settings
from config import CHROMEDRIVER_PATH, START_URL, COOKIES_PATH, DOWNLOAD_FOLDER, MAX_WORKERS, FILE_EXTENSIONS

# Функция для сохранения новых настроек
def save_new_settings():
    chromedriver_path = entry_chromedriver_path.get()
    start_url = entry_start_url.get()
    cookies_path = entry_cookies_path.get()
    download_folder = entry_download_folder.get()
    max_workers = int(entry_max_workers.get())
    file_extensions = entry_file_extensions.get().split(',')

    if chromedriver_path and start_url and cookies_path and download_folder and max_workers and file_extensions:
        save_settings(
            chromedriver_path,
            start_url,
            cookies_path,
            download_folder,
            max_workers,
            file_extensions
        )
        messagebox.showinfo("Информация", "Настройки успешно сохранены.")
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

# Загрузка сохранённых настроек
def load_current_settings():
    settings = load_settings()
    
    entry_chromedriver_path.delete(0, tk.END)
    entry_chromedriver_path.insert(0, settings.get("CHROMEDRIVER_PATH", "path/to/chromedriver"))
    
    entry_start_url.delete(0, tk.END)
    entry_start_url.insert(0, settings.get("START_URL", "http://example.com"))
    
    entry_cookies_path.delete(0, tk.END)
    entry_cookies_path.insert(0, settings.get("COOKIES_PATH", "cookies/cookies.json"))
    
    entry_download_folder.delete(0, tk.END)
    entry_download_folder.insert(0, settings.get("DOWNLOAD_FOLDER", "downloads"))
    
    entry_max_workers.delete(0, tk.END)
    entry_max_workers.insert(0, settings.get("MAX_WORKERS", 4))
    
    entry_file_extensions.delete(0, tk.END)
    entry_file_extensions.insert(0, ', '.join(settings.get("FILE_EXTENSIONS", ['.docx', '.pdf', '.xlsx'])))

# Главный интерфейс
root = tk.Tk()
root.title("Настройки скачивания файлов")

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

button_save_settings = tk.Button(root, text="Сохранить настройки", command=save_new_settings)
button_save_settings.pack(pady=10)

# Загрузка сохранённых настроек при старте
load_current_settings()

root.mainloop()
