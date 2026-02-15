import sqlite3
from ui import clear_screen, read_key
from db import log_action, DB_PATH

def get_completed_count():
    
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 1")
        count = cur.fetchone()[0]
        return count

def view():
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id, content FROM tasks WHERE status = 0")
        rows = cursor.fetchall()

    if not rows:
        print("00 | [null]")
    else:
        for row_id, content in rows:
            print(f"{row_id:<3} {content}")

def add():
    
    clear_screen()
    print("new task:")
    
    text = input("\n[q] > ").strip()

    if text == "q" or text == "":
        return

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO tasks (content, status) VALUES (?, 0)", (text,))
        log_action(conn)

def complete():
        
    clear_screen()
    view()
        
    task_id = input("\n[q] enter id to complete > ").strip()
        
    if task_id == "q" or task_id == "":
        return
            
    if task_id.isdigit():
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("UPDATE tasks SET status = 1 WHERE id = ?", (task_id,))
            log_action(conn)

def edit():
    
    clear_screen()
    view()
    task_id = input("\n[q] enter id to edit > ").strip()
    
    if not task_id.isdigit():
        return

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT content FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
    
        if row:
            print(f"\nold: {row[0]}")
            new_text = input("new: ").strip()
            if new_text:
                conn.execute("UPDATE tasks SET content = ? WHERE id = ?", (new_text, task_id))
                log_action(conn)

def run():
    
    while True:
        
        clear_screen()
        view()
        
        done_count = get_completed_count()
        print(f"\ncompleted: {done_count}")
        print("\n[q] [add] [edit] [complete] ", end="", flush=True)
        
        choice = read_key().lower()
        
        if choice == "q":
            break
        elif choice == "a":
            add()
        elif choice == "c":
            complete()
        elif choice == "e":
            edit()