import os
import threading

def check():
	print(threading.current_thread().ident)
	p = os.popen("ls")
	print(p.readlines())
	threading.Timer(2, check).start()
threading.Timer(2, check).start()
