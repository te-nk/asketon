import sqlite3
from datetime import datetime, timedelta
from ui import clear_screen, read_key
from db import DB_PATH, log_action

def db_get(query, params=()):
	with sqlite3.connect(DB_PATH) as conn:
		return conn.execute(query, params).fetchall()

def db_run(query, params=()):
	with sqlite3.connect(DB_PATH) as conn:
		conn.execute(query, params)
		log_action(conn)
		conn.commit()

def get_now():
	
	ish_now = datetime.now() + timedelta(hours=4)
	return ish_now.strftime("%y-%m-%d %H:%M")

def transaction(t_type):
	
	clear_screen()
	
	print(f"{t_type}")
	acc_name = input("\naccount: ").strip().lower()
	
	if not db_get("SELECT name FROM accounts WHERE name=?", (acc_name,)):
		print(f"\nno account {acc_name}"); read_key(); return

	try:
		amount = int(input("amount:  "))
		note = input("note:    ")
	except ValueError: return

	current_res = db_get("SELECT balance FROM accounts WHERE name=?", (acc_name,))
	current_balance = current_res[0][0]
	
	now = get_now()
	
	if t_type == "income":
		
		db_run("UPDATE accounts SET balance = balance + ? WHERE name=?", (amount, acc_name))
		db_run("INSERT INTO transactions (date, type, amount, acc_to, note) VALUES (?,?,?,?,?)",(now, 'income', amount, acc_name, note))
	else:
		
		if current_balance - amount < 0:
			print(f"\nnot enough money ({current_balance})")
			read_key()
			return
		
		db_run("UPDATE accounts SET balance = balance - ? WHERE name=?", (amount, acc_name))
		db_run("INSERT INTO transactions (date, type, amount, acc_from, note) VALUES (?,?,?,?,?)",(now, 'expense', amount, acc_name, note))

def transfer():
	
	clear_screen()
	
	print("transfer\n")
	f = input("from:   ").strip().lower()
	t = input("to:     ").strip().lower()
	
	try:
		amt = int(input(f"amount: "))
		
		res_f = db_get("SELECT balance FROM accounts WHERE name=?", (f,))
		if not res_f: return
	
		current_f = res_f[0][0]

		if current_f - amt < 0:
			print(f"\nlow balance on {f}: {current_f}")
			read_key()
			return
		
	except ValueError: return

	now = get_now()
	
	db_run("UPDATE accounts SET balance = balance - ? WHERE name=?", (amt, f))
	db_run("UPDATE accounts SET balance = balance + ? WHERE name=?", (amt, t))
	db_run("INSERT INTO transactions (date, type, amount, acc_from, acc_to, note) VALUES (?,?,?,?,?,?)",
		  (now, 'transfer', amt, f, t, ' '))

def account_settings():
	
	while True:
		
		clear_screen()
		
		accs = db_get("SELECT name, balance, currency FROM accounts")
		for n, b, c in accs:
			print(f"{n:<7} {b} {c}")
		
		print("\n[q] [new] [delete] ", end="", flush=True)
		key = read_key().lower()
		if key == "q": break
		elif key == "n":
			name = input("\n\nname: ").strip().lower()
			cur = input("currency: ").strip().lower() or " "
			if name: db_run("INSERT OR IGNORE INTO accounts VALUES (?, 0, ?)", (name, cur))
		elif key == "d":
			name = input("\n\ndelete: ").strip().lower()
			res = db_get("SELECT balance FROM accounts WHERE name=?", (name,))
			if res and res[0][0] == 0:
				db_run("DELETE FROM accounts WHERE name=?", (name,))
			else:
				print("no account or balance not zero")
				read_key()

def commands():
	
	clear_screen()
	
	print("[i] - income\n\n[e] - expense\n\n[t] - transfer\n\n[s] - settings\n")
		
	read_key()
	
def main_screen():
	
	now_with_offset = datetime.now() + timedelta(hours=4)
		
	cur_month = now_with_offset.strftime("%y-%m")
	logs = db_get("SELECT date, type, amount, acc_from, acc_to, note FROM transactions WHERE date LIKE ? ORDER BY id ASC", (f"{cur_month}%",))
		
	if not logs:
			print("no data in this month")
	else:
		
		for d, t, a, f, to, n in logs:
			if t == "income":
				acc_info = f"{to}"
			
			elif t == "expense":
				acc_info = f"{f}"
			
			else:
				acc_info =f"{f} > {to}"
				
			print(f"{d[6:]} {t[:3]} {acc_info} {a} {n}")
		
	accs = db_get("SELECT name, balance, currency FROM accounts")
	print("\n",end="")
	for name, bal, cur in accs:
		print(f"{name:<7} {bal} {cur}")
		
	print("\n[q] [cmd] ", end="", flush=True)

def run():
	
	while True:
		
		clear_screen()
		
		main_screen()
		
		key = read_key().lower()
		
		if key == "q":
			break
		elif key == "i":
			transaction("income")
		elif key == "e":
			transaction("expense")
		elif key == "t":
			transfer()
		elif key == "s":
			account_settings()
		elif key == "c":
			commands()
