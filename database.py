import hashlib
import sqlite3
import os

def init_db():
    # Check if the database file exists
    db_file = 'markdown_app.db'
    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' does not exist. Creating it...")

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT NOT NULL)''')

    # Create notes table
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  timestamp TEXT NOT NULL,
                  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE)''')

    # Enable foreign key constraints
    c.execute("PRAGMA foreign_keys = ON")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_file}' initialized successfully.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def register_user(username, hashed_password):
    conn = sqlite3.connect('markdown_app.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, hashed_password):
    conn = sqlite3.connect('markdown_app.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == hashed_password

def get_notes(username):
    conn = sqlite3.connect('markdown_app.db')
    c = conn.cursor()
    c.execute("SELECT title, content FROM notes WHERE username=?", (username,))
    notes = c.fetchall()
    conn.close()
    return notes

def save_note(username, title, content, timestamp):
    conn = sqlite3.connect('markdown_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (username, title, content, timestamp) VALUES (?, ?, ?, ?)",
              (username, title, content, timestamp))
    conn.commit()
    conn.close()

def delete_note(username, title):
    conn = sqlite3.connect('markdown_app.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE username=? AND title=?", (username, title))
    conn.commit()
    conn.close()

