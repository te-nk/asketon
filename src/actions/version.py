from ui import read_key
import time

def step():
	time.sleep(0.02)

def render():
	
	render = r"""
           __       __
 ___ ____ / /_____ / /____  ___
/ _ `(_-</  '_/ -_) __/ _ \/ _ \
\_,_/___/_/\_\\__/\__/\___/_//_/

v0.6               github: te-nk
"""

	for i in render.strip("\n").split("\n"):
		print(i)
		step()

def run():

    render()
      
    read_key()