import sqlite3

DATABASE_NAME = 'cake_sales.db'

def create_database():
    conn = sqlite3.connect('cake_sales.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regions
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT)
                        ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cake_types
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT)
                        ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date DATE NOT NULL,
            region_id INTEGER NOT NULL,
            cake_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (region_id) REFERENCES regions(id),
            FOREIGN KEY (cake_id) REFERENCES cakes(id)
        )
    ''')
    conn.commit()
    conn.close()
    
def add_region(region_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO regions (name) VALUES (?)", (region_name,))
        # cursor.execute("SELECT id FROM regions WHERE name=?", (region_name,))
        region_id = cursor.fetchone()[0]
        return region_id
    except TypeError:
        pass
    conn.commit()
    conn.close()    
    