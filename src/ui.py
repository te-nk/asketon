import os
import tty
import sys
import termios
import time

def clear_screen():
	
    os.system("clear")
	
def render_out():
    
    for i in range(10):
        sys.stdout.write("\r\033[2K\033[1A")
        sys.stdout.flush() 
        time.sleep(0.02)

def read_key():
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

