import sqlite3

def create_connection(db_file):
    """Crea una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    """Crea las tablas necesarias en la base de datos."""
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS character_detail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        race TEXT NOT NULL,
        height DECIMAL NOT NULL,
        character_id INTEGER NOT NULL,
        FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    ''')

    conn.commit()

db_file = "database.db"
conn = create_connection(db_file)
create_tables(conn)
conn.close()

print("Database and tables created successfully.")
