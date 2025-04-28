import sqlite3

DATABASE_NAME = 'cake_sales.db'

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_database():
    conn = sqlite3.connect('cake_sales.db')
    cursor = conn.cursor()

def initialize_database():
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO regions (name) VALUES (?)", (region_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Region '{region_name}' already exists.")
        pass # Region already exists
    finally:
        conn.close()
        
def add_cake_type(cake_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cake_types (name) VALUES (?)", (cake_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Cake type '{cake_name}' already exists.")
        pass # Cake type already exists
    finally:
        conn.close()
        
def add_sale(sale_date, region_name, cake_name, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM regions WHERE name=?", (region_name,))
    region_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM cake_types WHERE name=?", (cake_name,))
    cake_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO sales (sale_date, region_id, cake_id, quantity) VALUES (?, ?, ?, ?)", (sale_date, region_id, cake_id, quantity))    
    conn.commit()
    conn.close()