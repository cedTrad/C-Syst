import sqlite3

def init_db():
    """
    Initialize the database by creating the necessary tables if they do not exist.
    """
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            positionAmt REAL,
            entryPrice REAL,
            currentPrice REAL,
            unrealizedProfit REAL,
            leverage REAL,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            total_wallet_balance REAL,
            total_initial_margin REAL,
            total_unrealized_profit REAL,
            available_balance REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_event(event_type, event_time, symbol, side, order_type, quantity, price, result):
    """
    Log an event in the 'events' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (event_type, event_time, symbol, side, order_type, quantity, price, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (event_type, event_time, symbol, side, order_type, quantity, price, result))
    conn.commit()
    conn.close()

def log_position(symbol, positionAmt, entryPrice, currentPrice, unrealizedProfit, leverage, status='open'):
    """
    Log a position in the 'positions' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO positions (symbol, positionAmt, entryPrice, currentPrice, unrealizedProfit, leverage, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (symbol, positionAmt, entryPrice, currentPrice, unrealizedProfit, leverage, status))
    conn.commit()
    conn.close()

def update_position_status(position_id, status):
    """
    Update the status of a position in the 'positions' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE positions
        SET status = ?
        WHERE id = ?
    ''', (status, position_id))
    conn.commit()
    conn.close()

def log_portfolio_snapshot(timestamp, total_wallet_balance, total_initial_margin, total_unrealized_profit, available_balance):
    """
    Log a snapshot of the portfolio in the 'portfolio_history' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO portfolio_history (timestamp, total_wallet_balance, total_initial_margin, total_unrealized_profit, available_balance)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, total_wallet_balance, total_initial_margin, total_unrealized_profit, available_balance))
    conn.commit()
    conn.close()

def get_all_events():
    """
    Retrieve all events from the 'events' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return events

def get_all_positions():
    """
    Retrieve all positions from the 'positions' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM positions')
    positions = cursor.fetchall()
    conn.close()
    return positions

def get_portfolio_history():
    """
    Retrieve all portfolio snapshots from the 'portfolio_history' table.
    """
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM portfolio_history')
    history = cursor.fetchall()
    conn.close()
    return history

