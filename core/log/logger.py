import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'id': record.id,
            'time': self.formatTime(record, self.datefmt),
            'event': record.event,
            'username': record.username  # По умолчанию username = None (null в JSON)
        }
        return json.dumps(log_record)

# Настройка логирования
logger = logging.getLogger("jsonLogger")
logger.setLevel(logging.INFO)

# Обработчик для записи в файл
file_handler = logging.FileHandler('log.json')
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
