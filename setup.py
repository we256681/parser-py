from setuptools import setup, find_packages

setup(
    name="file-downloader",  # Название вашего проекта
    version="0.1",  # Версия проекта
    description="A Python project for downloading files using Selenium",  # Краткое описание проекта
    author="Your Name",  # Ваше имя
    author_email="your.email@example.com",  # Ваш email
    packages=find_packages(),  # Поиск всех пакетов в проекте
    install_requires=[  # Список зависимостей, которые требуются для работы проекта
        'selenium>=4.1.0',
    ],
    entry_points={  # Точка входа, если проект представляет собой команду CLI
        'console_scripts': [
            'file-downloader=src.main:start_download',  # Пример использования в качестве CLI
        ],
    },
    classifiers=[  # Метаданные о проекте
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Минимальная версия Python
)
