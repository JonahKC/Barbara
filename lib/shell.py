import threading
import importlib as imp
import time
import asyncio
import code


def start(clnt):
	global client
	client = clnt
	
	time.sleep(5)
	print("Started shell")
	evalThread = threading.Thread(target=startEvalLoop, name="Thread-ShellEval")
	evalThread.start()

def startEvalLoop():
	loop = asyncio.new_event_loop()
	asyncio.run_coroutine_threadsafe(evalLoop(loop), loop)
	loop.run_forever()

async def evalLoop(loop):
	print("Started shell evaluation")
	while True:
		cmd = input(">>>")
		if(cmd=="BRK"): break
		if(cmd=="RFILE"):
			imp.reload(code)
			await code.main(client)
		else:
			try:
				eval(cmd)
			except Exception as err:
				print("Error: {0}".format(err))
	print("Exited Shell Evaluation")
	loop.stop()