import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'id': record.id,
            'time': self.formatTime(record, self.datefmt),
            'event': record.event,
            'username': record.username  # По умолчанию username = None (null в JSON)
        }
        return json.dumps(log_record)
    
    def formatTime(self, record, datefmt=None):
        # Форматируем время без миллисекунд
        return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

# Настройка логирования
logger = logging.getLogger("jsonLogger")
logger.setLevel(logging.INFO)

# Обработчик для записи в файл
file_handler = logging.FileHandler('log.json', mode='a')
file_handler.setLevel(logging.INFO)

# Применяем JSONFormatter
formatter = JSONFormatter()
file_handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger.addHandler(file_handler)

# Функция для логирования событий
def log_connection(id):
    extra = {
        'id': id,
        'event': 'connection',
        'username': None  # Устанавливаем username в None для события подключения
    }
    logger.info("Connection event", extra=extra)

def log_authorization(id, username):
    extra = {
        'id': id,
        'event': 'authorization',
        'username': username
    }
    logger.info("Authorization event", extra=extra)

def get_logs_as_json(file_path='log.json'):
    try:
        with open(file_path, 'r') as log_file:
            # Читаем содержимое файла построчно
            logs = log_file.readlines()
            # Парсим каждую строку как JSON
            logs_json = [json.loads(log.strip()) for log in logs]
            return logs_json
    except FileNotFoundError:
        return {"error": "Log file not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding log file"}
    
def delete_logs(n, file_path='log.json'):
    try:
        with open(file_path, 'r') as log_file:
            logs = log_file.readlines()
        
        # Оставляем только те записи, которые остаются после удаления n первых
        remaining_logs = logs[n:]

        # Перезаписываем файл с оставшимися логами
        with open(file_path, 'w') as log_file:
            log_file.writelines(remaining_logs)
        
        print(f"Deleted {n} log(s).")
    except FileNotFoundError:
        print("Log file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")