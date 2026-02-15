import time
from db import get_total_actions

def step():
	time.sleep(0.02)

def render():
	
	render = r"""
           __       __
 ___ ____ / /_____ / /____  ___
/ _ `(_-</  '_/ -_) __/ _ \/ _ \
\_,_/___/_/\_\\__/\__/\___/_//_/

[finance]  [workout]  [tasks]

[cloud]  [quit]  [ver]

"""

	for i in render.strip("\n").split("\n"):
		print(i)
		step()

def promt():
	
	count = get_total_actions()
	print(f"\n[{count}] > ", end="", flush=True)

def run():
	
	render()
	promt()
