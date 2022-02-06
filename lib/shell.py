#import time, asyncio, threading, psutil
#import readline, console
import sys, threading, time, asyncio
#import humanize
#import subprocess
#from time import sleep
#from console.screen import sc
#from console.progress import ProgressBar
#from console import TermStack
#import lib.graph as graph

UP = '\033[F'

def write(string: str, flush: bool=True) -> None:
  sys.stdout.write(string)
  if flush:
    sys.stdout.flush()

def run():
  dataThread = threading.Thread(target=dataLoop, name='Thread-ShellEval')
  evalThread = threading.Thread(target=startEvalLoop, name="Thread-ShellEval")
  evalThread.start()
  dataThread.start()

def initialize(_bot):
  global bot, stdscr
  time.sleep(5)
  bot = _bot
  bot.load_extension("code")

def startEvalLoop():
  loop = asyncio.new_event_loop()
  asyncio.run_coroutine_threadsafe(evalLoop(loop), loop)
  loop.run_forever()

def dataLoop():
  pass
  #global stdscr
  #time.sleep(1)
  #cpuProgress = ProgressBar()
  #ramProgress = ProgressBar()
  #while True:
    #graph.writeAt(
    #  str(cpuProgress(psutil.cpu_percent(1) / psutil.cpu_count())) + 
    #  " CPU",
    #  0, 50
    #)
    #graph.writeAt(
    #  str(ramProgress(psutil.virtual_memory().percent)) + 
    #  f" RAM " + 
    #  humanize.naturalsize(psutil.virtual_memory().used) + "/" +
    #  humanize.naturalsize(psutil.virtual_memory().total),
    #  0, 79
    #)

async def evalLoop(loop):
  #global bot
  #print("Started shell evaluation")
  #for i in range(10):
    #print(str(i))
    #time.sleep(0.1)
  #print(graph.input_location)
  #graph.gotoInput()
  #while True:
  #  cmd = sys.stdin.readline()
  #  if cmd in ("BRK", "break"):
  #    break
  #  elif cmd in ("RFL", "runtimefile"):
  #    bot.reload_extension("code")
  #    cog = bot.get_cog("RuntimeFile")
  #    await cog.main()
  #  elif cmd in ("RST", "restart"):
  #    sys.exit(0)
  #  elif cmd.startswith("SHL "):
  #    print(subprocess.run(cmd[5:]))
  #  elif cmd.startswith("shell "):
  #    print(subprocess.run(cmd[8:]))
  #  else:
  #    try:
  #      exec(cmd)
  #    except Exception as err:
  #      print("Error: {0}".format(err))
  #print("Exited Shell Evaluation")
  loop.stop()