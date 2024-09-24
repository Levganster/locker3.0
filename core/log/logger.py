import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'id': getattr(record, 'id', None),
            'time': self.formatTime(record, self.datefmt),
            'event': getattr(record, 'event', 'Unknown'),
            'username': getattr(record, 'username', None)  # По умолчанию username = None
        }
        return json.dumps(log_record)
    
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

# Промежуточное хранилище для логов
logs_buffer = []

class ReverseOrderHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logs_buffer.append(log_entry)
    
    def flush_to_file(self):
        with open('log.json', 'w') as f:
            # Записываем логи в обратном порядке
            for log in reversed(logs_buffer):
                f.write(log + '\n')

# Настройка логирования
logger = logging.getLogger("jsonLogger")
logger.setLevel(logging.INFO)

# Используем кастомный обработчик вместо стандартного FileHandler
reverse_handler = ReverseOrderHandler()
formatter = JSONFormatter()
reverse_handler.setFormatter(formatter)
logger.addHandler(reverse_handler)

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

def log_disconnection(id, username):
    extra = {
        'id': id,
        'event': 'disconnection',
        'username': username
    }
    logger.info("Disconnection event", extra=extra)


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