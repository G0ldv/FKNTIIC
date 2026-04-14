import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, full_name=None, username=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, full_name, username, phone) 
            VALUES (?, ?, ?, (SELECT phone FROM users WHERE user_id = ?))
        ''', (user_id, full_name, username, user_id))
        conn.commit()
    except Exception as e:
        print(f"Помилка бази: {e}")
    finally:
        conn.close()

def get_users_count():
    """Повертає загальну кількість користувачів для статистики"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_users():
    """Повертає список усіх ID користувачів для розсилки"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

def get_all_users_full():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, full_name, username, phone FROM users')
    users = cursor.fetchall()
    conn.close()
    return users