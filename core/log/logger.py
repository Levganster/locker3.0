import json
from datetime import datetime
import os

LOG_FILE = 'logs.json'


def log_event(id: str, event: str, username: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Без миллисекунд
    log_entry = {
        'id': id,
        'time': current_time,
        'event': event,
        'username': username
    }
    save_log(log_entry)

def log_connection(id: str):
    log_event(id, "connection", None)
def log_authorization(id: str, username: str):
    log_event(id, "authorization", username)
def log_disconnection(id: str, username: str):
    log_event(id, "disconnection", username)

def save_log(log_entry):
    # Чтение текущего файла логов
    logs = read_logs()

    # Добавление новой записи в начало списка
    logs.insert(0, log_entry)

    # Сохранение в файл
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)


def read_logs():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, 'r') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    return logs


def delete_logs(n: int):
    logs = read_logs()

    if len(logs) >= n:
        logs = logs[n:]  # Удаляем первые n записей
    else:
        logs = []

    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)