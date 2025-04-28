import sqlite3

DATABASE_NAME = 'cake_sales.db'

def create_database():
    conn = sqlite3.connect('cake_sales.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT,
                      region TEXT,
                      heart_cakes INTEGER,
                      coconut_cakes INTEGER,
                      mobile_cakes INTEGER,
                      block_cakes INTEGER,
                      star_cakes INTEGER,
                      queen_cakes INTEGER,
                      sweet_cakes INTEGER)''')
    conn.commit()
    conn.close()