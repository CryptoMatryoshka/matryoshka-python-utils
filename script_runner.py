import subprocess
import time
import logging
from dotenv import load_dotenv
import os
from datetime import datetime
from random import randint

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение списка скриптов из переменной окружения
SCRIPTS_ENV = os.getenv('SCRIPTS')
if not SCRIPTS_ENV:
    raise ValueError("Список скриптов не найден в переменных окружения. "
                     "Проверьте наличие SCRIPTS переменной в .env файле.")

# Преобразование строки скриптов в список
scripts = SCRIPTS_ENV.split(',')

# Проверяем лежит ли python в .venv
python_exec_file_1 = "./venv/Scripts/python.exe"
python_exec_file_2 = "../venv/Scripts/python.exe"
if os.path.isfile(python_exec_file_1):
    python_exec_file = python_exec_file_1
elif os.path.isfile(python_exec_file_2):
    python_exec_file = python_exec_file_2
else:
    python_exec_file = "python"

def run_script(script_path):
    logging.info(f"Используем python скрипт {python_exec_file}")

    logging.info(f"Стартуем скрипт: {script_path}...")
    subprocess.run([python_exec_file, script_path], check=True)


def run_scripts_in_infinite_loop():
    iteration = 0
    # ditc для хранения времени последнего запуска script_conf:datatime
    script_execution_dict = {}
    for script_conf in scripts:
        script_execution_dict[script_conf] = datetime.min

    logging.info(f"Начинаем пускать скрипты!")
    while True:
        iteration += 1
        try:
            for script_conf in scripts:
                # Путь до скрипта
                script_path = script_conf.split(':')[0]
                # Интервал проверки в секундах
                check_interval_seconds = int(script_conf.split(':')[1])

                # Считаем сколько времени прошло
                past_seconds = int((script_execution_dict[script_conf] - datetime.now()).total_seconds())
                # Добавляем rand чтобы, не палиться как робот
                if past_seconds > check_interval_seconds + randint(1, 30):
                    # Сохраняем время запуска
                    script_execution_dict[script_conf] = datetime.now()

                    logging.info(f"Пускаем скрипт: {script_path}")
                    run_script(script_path)
                    logging.info(f"Скрипт отработал: {script_path}")

            # Таймаут перед следующим запуском
            time.sleep(1)
        except subprocess.CalledProcessError as e:
            logging.error(f"Скрипт {script_path} упал. Перезапускаем... {e}")
            # Задержка перед перезапуском
            time.sleep(5)
