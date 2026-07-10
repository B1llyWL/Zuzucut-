import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')
TEMPLATES_FILE = os.path.join(os.path.dirname(__file__), 'templates.json')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS clients (client_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_message_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS banned_users (user_id INTEGER PRIMARY KEY, reason TEXT DEFAULT '')''')

def get_admin_id():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT value FROM config WHERE key="admin_id"')
        row = c.fetchone()
        return int(row[0]) if row else None

def set_admin_id(admin_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO config (key, value) VALUES ("admin_id", ?)', (str(admin_id),))
        conn.commit()

def save_client(client_id, username, first_name):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO clients (client_id, username, first_name, last_message_time) VALUES (?, ?, ?, CURRENT_TIMESTAMP)''', (client_id, username, first_name))
        conn.commit()

def get_templates():
    if not os.path.exists(TEMPLATES_FILE):
        return {}
    with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_templates(templates):
    with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)

def get_prices():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT value FROM config WHERE key="prices_text"')
        row = c.fetchone()
        if row:
            return row[0]
    return ("Ознакомься с расценками:\n\n📌 Скетч-арт с плоским покрасом:\n• Хед — 150₽\n• По пояс — 300₽\n• Полнорост — 500₽\n\n📌 Полноценный арт:\n• Хед — 300₽\n• По пояс — 600₽\n• Полнорост — 1000₽\n\n📌 Полноценный арт с фоном:\n• Хед — 450₽\n• По пояс — 700₽\n• Полнорост — 1500₽\n\n📌 Фон:\n1. С простой заливкой — бесплатно\n2. Без сильной проработанности — +100-250₽\n3. Коллаж — +70₽\n\n📌 Дополнительные факторы:\n1. Излишняя детализация — доплата\n2. Сложный ракурс — доплата\n3. +Персонаж — 100% оплаты\n\n🔗 Актуальные цены: https://t.me/Zuzucut")

def set_prices(text):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO config (key, value) VALUES ("prices_text", ?)', (text,))
        conn.commit()

def ban_user(user_id, reason=""):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO banned_users (user_id, reason) VALUES (?, ?)', (user_id, reason))
        conn.commit()

def unban_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM banned_users WHERE user_id=?', (user_id,))
        conn.commit()

def is_banned(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM banned_users WHERE user_id=?', (user_id,))
        return c.fetchone() is not None
