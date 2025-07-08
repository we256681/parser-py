#!/usr/bin/env python3
"""
Скрипт для проверки и тестирования ChromeDriver
"""

import os
import sys
import subprocess
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def check_chrome_version():
    """Проверка версии Chrome"""
    try:
        # Для Ubuntu/Debian
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        
        # Альтернативная команда
        result = subprocess.run(['chromium-browser', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
            
    except FileNotFoundError:
        pass
    
    return "Chrome не найден"

def check_chromedriver_system():
    """Проверка системного ChromeDriver"""
    chromedriver_path = shutil.which('chromedriver')
    if chromedriver_path:
        try:
            result = subprocess.run([chromedriver_path, '--version'], 
                                  capture_output=True, text=True)
            return chromedriver_path, result.stdout.strip()
        except:
            return chromedriver_path, "Ошибка при получении версии"
    return None, "ChromeDriver не найден в системе"

def check_chromedriver_binary():
    """Проверка chromedriver-binary"""
    try:
        import chromedriver_binary
        print("✓ chromedriver-binary найден")
        
        # Попытка создать драйвер
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        print("✓ ChromeDriver через chromedriver-binary работает")
        driver.quit()
        return True
        
    except ImportError:
        print("✗ chromedriver-binary не установлен")
        return False
    except Exception as e:
        print(f"✗ Ошибка при тестировании chromedriver-binary: {e}")
        return False

def check_webdriver_manager():
    """Проверка webdriver-manager"""
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager найден")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.google.com")
        print("✓ ChromeDriver через webdriver-manager работает")
        driver.quit()
        return True
        
    except ImportError:
        print("✗ webdriver-manager не установлен")
        return False
    except Exception as e:
        print(f"✗ Ошибка при тестировании webdriver-manager: {e}")
        return False

def main():
    print("=== Проверка ChromeDriver ===\n")
    
    # Проверка версии Chrome
    chrome_version = check_chrome_version()
    print(f"Версия Chrome: {chrome_version}")
    
    # Проверка системного ChromeDriver
    chromedriver_path, chromedriver_version = check_chromedriver_system()
    if chromedriver_path:
        print(f"Системный ChromeDriver: {chromedriver_path}")
        print(f"Версия: {chromedriver_version}")
    else:
        print("Системный ChromeDriver не найден")
    
    print("\n=== Тестирование методов ===\n")
    
    # Тестирование различных методов
    methods = [
        ("chromedriver-binary", check_chromedriver_binary),
        ("webdriver-manager", check_webdriver_manager)
    ]
    
    working_methods = []
    for method_name, test_func in methods:
        print(f"\nТестирование {method_name}:")
        if test_func():
            working_methods.append(method_name)
    
    print(f"\n=== Результаты ===")
    print(f"Рабочие методы: {', '.join(working_methods) if working_methods else 'Нет'}")
    
    # Рекомендации
    print(f"\n=== Рекомендации ===")
    if "chromedriver-binary" in working_methods:
        print("✓ Рекомендуется использовать chromedriver-binary")
        print("  Установка: pip install chromedriver-binary")
    elif "webdriver-manager" in working_methods:
        print("✓ Рекомендуется использовать webdriver-manager")
        print("  Установка: pip install webdriver-manager")
    else:
        print("✗ Необходимо решить проблемы с ChromeDriver")
        print("  Попробуйте:")
        print("  1. sudo apt update && sudo apt install chromium-browser chromium-chromedriver")
        print("  2. pip install webdriver-manager")
        print("  3. Проверьте совместимость версий Chrome и ChromeDriver")

if __name__ == "__main__":
    main()