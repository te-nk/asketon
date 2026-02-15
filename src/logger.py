from datetime import datetime, timedelta

LOG_FILE = "asketon.log"

def log(level, message):
	now = datetime.now() + timedelta(hours=4)
	timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
	with open(LOG_FILE, "a") as f:
		f.write(f"{timestamp} | {level:<7} | {message}\n")
