import time
from collections import defaultdict

# Хранилище сообщений (сбрасывается при перезапуске бота)
user_messages = defaultdict(list)

# Настройки
MAX_MESSAGES = 20
TIME_WINDOW = 60
BLOCK_TIME = 300

# Блоклист
blocked_users = {}


def is_spamming(user_id: int) -> bool:
    """Проверка на спам"""
    current_time = time.time()

    # Проверка на блок пользователя
    if user_id in blocked_users:
        if current_time < blocked_users[user_id]:
            return True
        else:
            # разблокировка
            del blocked_users[user_id]

    # Получаем сообщения пользователя
    messages = user_messages[user_id]

    # Удаляем старые сообщения (старше TIME_WINDOW)
    messages = [t for t in messages if current_time - t < TIME_WINDOW]
    user_messages[user_id] = messages

    # Проверка лимита
    if len(messages) >= MAX_MESSAGES:
        # Блокировка
        blocked_users[user_id] = current_time + BLOCK_TIME
        return True

    # Добавление текущего сообщения
    messages.append(current_time)
    return False


def get_block_time(user_id: int) -> int:
    """Возвращает время разблокировки"""
    if user_id in blocked_users:
        remaining = int(blocked_users[user_id] - time.time())
        return max(0, remaining)
    return 0


def unblock_user(user_id: int):
    """Разблокировка пользователя"""
    if user_id in blocked_users:
        del blocked_users[user_id]
