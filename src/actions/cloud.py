import subprocess
import socket
import os
from datetime import datetime, timedelta
from ui import clear_screen, read_key
from logger import log

LASTB_FILE = ".last_backup"
    
def set_last_backup_time():
    
    now = datetime.now()
    local_time = now + timedelta(hours=4)
    time = local_time.strftime("%d.%m %H:%M")
    with open(LASTB_FILE, "w") as f:
        f.write(time)
        
def get_last_backup_time():
    
    if os.path.exists(LASTB_FILE):
        with open(LASTB_FILE, "r") as f:
            return f.read().strip()
    return "null"

def online():
    
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def fix_network():
    
    if not online():
        
        log("WARNING", "Network: Connection test failed (Offline)")
        print("no internet")
        return False
    print("checking network..", end=" ", flush=True)
    try:
        socket.gethostbyname('github.com')
        print("ok")
        return True
    except socket.gaierror:
        log("ERROR", "Network: DNS Resolution failed for github.com")
        print("dns fail.")
        print("patching /etc/resolv.conf...")
        try:
            with open('/etc/resolv.conf', 'w') as f:
                f.write("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")
            log("INFO", "Network: Patched /etc/resolv.conf")
            print("done")
            return True
        except PermissionError:
            log("ERROR", "Network: No root")
            print("failed (no root)")
            return False

def check_remote_updates():
    
    try:
        
        subprocess.run(["git", "fetch"], capture_output=True)
        
        res = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True).stdout.lower()
        
        if "behind" in res:
            return True
        return False
    except:
        return False

def status():
    
    has_update = check_remote_updates()
    
    last = get_last_backup_time()
        
    print(f"\nlast backup: {last}")
    
    if has_update:
        
        print("\nbehind cloud, press [r]")
        print("\n[q] [restore] ", end="", flush=True)
        
    else:
        
        print("\n[q] [upload] ", end="", flush=True)

def upload():
    
    print("upload..")
    
    set_last_backup_time()

    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", "upd"], capture_output=True)
    res = subprocess.run("git push", shell=True, capture_output=True, text=True)
    
    if res.returncode == 0:
        log("INFO", "Cloud: Data pushed to git")
        print("done")
    else:
        error_message = res.stderr.strip()
        log("ERROR", f"Cloud: Push failed: {error_message}")
        print("fail")
    print("\n[q] ", end="", flush=True)
    read_key()
    
def restore():
    
    print("download..")
    
    subprocess.run(["git", "pull"], capture_output=True)
    
    print("done")
    print("\n[q] ", end="", flush=True)
    read_key()

def run():
    
    if not fix_network():
        print("\n[q] ", end="", flush=True)
        read_key()
        return
    
    status()
    
    choice = read_key().lower()

    if choice == "u":

        clear_screen()
        upload()
        
    elif choice == "r":
        
        clear_screen()
        restore()
