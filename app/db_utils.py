import sqlite3

def init_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            event_time TEXT,
            symbol TEXT,
            side TEXT,
            order_type TEXT,
            quantity REAL,
            price REAL,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_event(event_type, event_time, symbol, side, order_type, quantity, price, result):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (event_type, event_time, symbol, side, order_type, quantity, price, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (event_type, event_time, symbol, side, order_type, quantity, price, result))
    conn.commit()
    conn.close()

def get_all_events():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return events

