from ui import clear_screen, read_key
from db import log_action, DB_PATH, EXERCISES
import sqlite3
		
def add_reps(choice_key):
	
	name = EXERCISES.get(choice_key)
	if not name: return

	print(f"\n\nnum of {name.lower()} > ", end="", flush=True)
	value = input().strip()
    
	if not value.isdigit(): return

	with sqlite3.connect(DB_PATH) as conn:

		conn.execute("UPDATE exercises SET count = count + ? WHERE name = ?", (int(value), name))
        
		log_action(conn)

def view():
	
	with sqlite3.connect(DB_PATH) as conn:
		data = dict(conn.execute("SELECT name, count FROM exercises").fetchall())

	for key, name in EXERCISES.items():

		count = data.get(name, 0)
		print(f"{key:<3} {name:<11} {count}")

	print("\n[q] [1] [2] [3] [4] ", end="", flush=True)

def run():
	
	while True:
		
		clear_screen()
		view()
        
		choice = read_key().lower()
        
		if choice == "q":
			break
        
		try:
			choice_int = int(choice)
			if choice_int in EXERCISES:
				add_reps(choice_int)
		except ValueError:
			continue
