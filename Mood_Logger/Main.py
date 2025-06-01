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

def ask_questions():
    print("\nHow are you feeling today?")
    print("a) Happy")
    print("b) Okay")
    print("c) Tired")
    print("d) Stressed")
    print("e) Sad")

    valid_moods = ["a", "b", "c", "d", "e"]
    while True:
        q1 = input("Choose your mood (a-e): ").strip().lower()
        if q1 in valid_moods:
            break
        else:
            print("Please enter a valid option (a, b, c, d, or e).")

    mood_score_map = {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1}
    mood_score = mood_score_map.get(q1, 0)

    q2 = ""
    while q2 not in ["yes", "no"]:
        q2 = input("Did you sleep well last night? (yes/no): ").strip().lower()
        if q2 not in ["yes", "no"]:
            print("Please answer with yes or no.")

    q3 = ""
    while q3 not in ["yes", "no"]:
        q3 = input("Did you get physical activity today? (yes/no): ").strip().lower()
        if q3 not in ["yes", "no"]:
            print("Please answer with yes or no.")

    q4 = input("Any additional notes you'd like to add? (Optional): ").strip()

    print("Would you like to receive encouragement messages or just a check-in?")
    print("a) Encouragement")
    print("b) Check-in only")

    while True:
        q5 = input("Choose (a/b): ").strip().lower()
        if q5 in ["a", "b"]:
            break
        else:
            print("Please enter 'a' or 'b'.")

    return {
        "emotional_state": q1,
        "mood_score": mood_score,
        "slept_well": q2,
        "active_today": q3,
        "note": q4,
        "needs_encouragement": q5
    }

def save_entry(entry):
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mood_entries (emotional_state, mood_score, slept_well, active_today, note, needs_encouragement)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        entry["emotional_state"],
        entry["mood_score"],
        entry["slept_well"],
        entry["active_today"],
        entry["note"],
        entry["needs_encouragement"]
    ))
    conn.commit()
    conn.close()
    print("💾 Entry saved successfully!\n")
