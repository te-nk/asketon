import sqlite3
from pathlib import Path
from logger import log

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ROOT_DIR / "asketon.db"

EXERCISES = {
	1: "pullups",
	2: "pushups",
	3: "squats",
	4: "legraises",
}

def init_db():
	
	try:
	
		with sqlite3.connect(DB_PATH) as conn:
	
			#stat
			conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value INTEGER)")
			conn.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('total_actions', 0)")
		
			#workout
			conn.execute("""
				CREATE TABLE IF NOT EXISTS exercises (
					name TEXT PRIMARY KEY,
					count INTEGER DEFAULT 0
				)
			""")
		
			#tasks
			conn.execute("""
				CREATE TABLE IF NOT EXISTS tasks (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					content TEXT NOT NULL,
					status INTEGER DEFAULT 0
				)
			""")
		
			#fill exercises
			for name in EXERCISES.values():
				conn.execute("INSERT OR IGNORE INTO exercises (name, count) VALUES (?, 0)", (name,))

			#finance
			conn.execute("""
				CREATE TABLE IF NOT EXISTS accounts (
					name TEXT PRIMARY KEY,
					balance INTEGER DEFAULT 0,
					currency TEXT DEFAULT 'usd'
				)
			""")
		
			conn.execute("""
				CREATE TABLE IF NOT EXISTS transactions (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					date TEXT,
					type TEXT,
					amount INTEGER,
					acc_from TEXT,
					acc_to TEXT,
					note TEXT
				)
			""")

			conn.execute("INSERT OR IGNORE INTO accounts (name, currency) VALUES ('cash', 'usd')")

		log("INFO", "Database: Connection and tables initialized.")
	
	except Exception as e:
		
		log("ERROR", f"Database: Initialization failed: {e}")

def log_action(conn):
	
	conn.execute("UPDATE meta SET value = value + 1 WHERE key = 'total_actions'")

def get_total_actions():
	
	with sqlite3.connect(DB_PATH) as conn:
		res = conn.execute("SELECT value FROM meta WHERE key = 'total_actions'").fetchone()
		
		return int(res[0]) if res else 0
