import sqlite3


def init_db():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotional_state TEXT,
            mood_score INTEGER,
            slept_well TEXT,
            active_today TEXT,
            note TEXT,
            needs_encouragement TEXT
        )
    ''')
    conn.commit()
    conn.close()

def show_welcome():
    print("🌟 Welcome to Daily Mood Logger with Encouragement Tracker 🌟\n")

def show_menu():
    print("\nWhat would you like to do?")
    print("1. Log a new mood")
    print("2. View mood history")
    print("3. Exit")
    print("4. Reset history")
    print("5. Edit an entry")
