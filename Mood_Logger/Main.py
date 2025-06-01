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

def generate_encouragement(entry):
    mood_map = {
        "a": "Happy",
        "b": "Okay",
        "c": "Tired",
        "d": "Stressed",
        "e": "Sad"
    }

    encouragement_map = {
        "a": "Keep enjoying your happiness and spread the joy!",
        "b": "It's okay to have an okay day. Keep moving forward!",
        "c": "Rest is important — take time to recharge, you deserve it!",
        "d": "Remember to breathe and take things one step at a time. You've got this!",
        "e": "It's okay to feel sad sometimes. Tomorrow is a new day with new possibilities."
    }

    check_in_message = "Thanks for checking in with yourself today. Remember, you're not alone."

    mood = mood_map.get(entry["emotional_state"], "Unknown")
    needs_encouragement = entry["needs_encouragement"]

    print("\n💡 Here's your encouragement message:\n")

    if needs_encouragement == "a":
        message = encouragement_map.get(entry["emotional_state"],
                                       "Keep taking care of yourself!")
        print("Because you're feeling {}, {}".format(mood, message))

        if entry["slept_well"] == "no":
            print("- Try to get some restful sleep soon; it helps your mind and body heal.")

        if entry["active_today"] == "no":
            print("- A little physical activity, even a short walk, can boost your mood.")

        if entry["note"]:
            print("- Thanks for sharing: \"{}\". Remember, expressing yourself helps!".format(entry['note']))

    else:
        print(check_in_message)

def get_entries_count():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mood_entries")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_average_mood():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(mood_score) FROM mood_entries")
    avg = cursor.fetchone()[0]
    conn.close()
    return avg

def view_history():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, emotional_state, slept_well, active_today, note FROM mood_entries")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\n📚 Mood History:")
        mood_map = {"a": "Happy", "b": "Okay", "c": "Tired", "d": "Stressed", "e": "Sad"}
        for row in rows:
            print("ID: {}, Mood: {}, Slept Well: {}, Active Today: {}, Note: {}".format(
                row[0], mood_map.get(row[1], 'Unknown'), row[2], row[3], row[4]))
    else:
        print("\n📭 No mood entries found yet.\n")

def reset_history():
    confirm = input("\n⚠️ Are you sure you want to delete all entries? This cannot be undone. (yes/no): ").strip().lower()
    if confirm == "yes":
        conn = sqlite3.connect("entries.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mood_entries")
        conn.commit()
        conn.close()
        print("🗑️ All entries have been deleted. History reset.\n")
    else:
        print("❌ Reset cancelled.\n")

def edit_entry():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, emotional_state, note FROM mood_entries")
    rows = cursor.fetchall()

    if not rows:
        print("\n📭 No entries to edit.\n")
        conn.close()
        return

    print("\n📝 Mood Entries:")
    for row in rows:
        print(f"ID: {row[0]}, Mood: {row[1]}, Note: {row[2]}")

    try:
        edit_id = int(input("\nEnter the ID of the entry you want to edit: ").strip())
    except ValueError:
        print("❌ Invalid input. Please enter a number.\n")
        conn.close()
        return

    cursor.execute("SELECT * FROM mood_entries WHERE id=?", (edit_id,))
    entry = cursor.fetchone()
    if not entry:
        print(f"❌ No entry found with ID {edit_id}.\n")
        conn.close()
        return

    mood_score_map = {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1}

    print("\nLeave input blank to keep current value.\n")

    new_mood = input(f"New emotional state (a-e) [current: {entry[1]}]: ").strip().lower()
    if new_mood == "":
        new_mood = entry[1]
    if new_mood not in mood_score_map:
        print("❌ Invalid mood input. Keeping current value.")
        new_mood = entry[1]
    new_score = mood_score_map.get(new_mood, 0)

    new_slept = input(f"Did you sleep well? (yes/no) [current: {entry[3]}]: ").strip().lower()
    if new_slept == "":
        new_slept = entry[3]

    new_active = input(f"Did you get physical activity? (yes/no) [current: {entry[4]}]: ").strip().lower()
    if new_active == "":
        new_active = entry[4]

    new_note = input(f"Note [current: {entry[5]}]: ").strip()
    if new_note == "":
        new_note = entry[5]

    new_encourage = input(f"Needs encouragement? (a=Encouragement, b=Check-in) [current: {entry[6]}]: ").strip().lower()
    if new_encourage == "":
        new_encourage = entry[6]
    if new_encourage not in ["a", "b"]:
        print("❌ Invalid encouragement input. Keeping current value.")
        new_encourage = entry[6]

    cursor.execute('''
        UPDATE mood_entries
        SET emotional_state=?, mood_score=?, slept_well=?, active_today=?, note=?, needs_encouragement=?
        WHERE id=?
    ''', (new_mood, new_score, new_slept, new_active, new_note, new_encourage, edit_id))

    conn.commit()
    conn.close()

    print("✅ Entry updated successfully!\n")

def main():
    init_db()
    show_welcome()
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            entry = ask_questions()
            save_entry(entry)
            generate_encouragement(entry)

            count = get_entries_count()
            avg = get_average_mood()

            print("📅 Total days logged: {}".format(count))
            if avg is not None:
                print("📊 Your average mood score so far is: {:.2f} out of 5".format(avg))
            else:
                print("📊 No mood scores recorded yet.")
            print("\nThank you for logging your mood today! Remember, every day is a new opportunity to feel better.\n")
        elif choice == "2":
            view_history()
        elif choice == "3":
            print("\n👋 Goodbye! Take care of yourself.\n")
            break
        elif choice == "4":
            reset_history()
        elif choice == "5":
            edit_entry()
        else:
            print("❌ Invalid choice. Please try again.")

main()

