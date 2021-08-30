import sys, readline, console, shutil, traceback
from time import sleep
import builtins as __builtin__

height = shutil.get_terminal_size().lines - 1

stdout_write_bytes = sys.stdout.buffer.write


# Some ANSI/VT100 Terminal Control Escape Sequences
CSI = b'\x1b['
CLEAR = CSI + b'2J'
CLEAR_LINE = CSI + b'2K'
SAVE_CURSOR = CSI + b's'
UNSAVE_CURSOR = CSI + b'u'



def emit(*args):
  stdout_write_bytes(b''.join(args))


def setScroll(n):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  return CSI + b'0;%dr' % n

def flush():
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  sys.stdout.flush()
  #emit(*constant_buffer)

def getHeight():
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  return height

def write(data, *, mode="t", encode="utf8", end="\n", file=sys.stdout):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  if(mode=="t"):
    data = str(data)
    if(type(data)==tuple):
      for i in data:
        emit(UNSAVE_CURSOR,i.encode(encode),end.encode(encode),  SAVE_CURSOR)
    else:
      emit(UNSAVE_CURSOR,data.encode(encode),end.encode(encode),  SAVE_CURSOR)
    flush()
  elif(mode == "b"):
    if(type(data)==tuple):
      for i in data:
        emit(UNSAVE_CURSOR,i,end.encode(encode),SAVE_CURSOR)
    else:
      emit(UNSAVE_CURSOR,data,end.encode(encode),SAVE_CURSOR)
    flush()
  else: raise TypeError("mode must be 't' or 'b'")
  gotoInput()
  flush()

def goto(x,y):
  return CSI+b'%d;%dH' % (y,x)

def setStatic(text,number=None):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  if(number==None):
    if(type(text)==str):
      text = text.encode("utf8")
    static_lines.append(text)
    updateStatic()
  elif(number>=len(static_lines)):
    raise IndexError
  else:
    if(type(text)==str):
      text = text.encode("utf8")
    static_lines[number] = text
    updateStatic(number)
  emit(setScroll(height - len(static_lines)))
  flush()

def getStatic():
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  return static_lines

def getConstantBuffer():
	global constant_buffer
	return constant_buffer

def setConstantBuffer(arr):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  constant_buffer = list(arr)

def writeAt(data, x, y, mode="t", encode="utf8", clear=False):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  if(mode=="t"):
    if(type(data)==tuple):
      for i in data:
        emit(goto(x,y))
				
        emit(i.encode(encode))
      emit(*gotoInput())
    else:
      emit(goto(x,y),data.encode(encode),*gotoInput())
    flush()
  elif(mode == "b"):
    if(type(data)==tuple):
      for i in data:
        emit(goto(x,y),i,*gotoInput())
    else:
      emit(goto(x,y),data,*gotoInput())
    flush()
  else: raise TypeError("mode must be 't' or 'b'")
  emit(goto(4,26))
  flush()

def gotoInput():
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  emit(goto(0,input_location[1]))#,CSI+b'1b',CSI+b'1d')
  flush()

def setInput(x,y,line=None):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  if not line: line = input_line
  input_location = [x,y]
  print(input_location)
  input_line=line

def updateStatic(line:int=None):
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  if(line==None):
    for i in range(len(static_lines)):
      if(i==input_line):
        emit(goto(0,height-i), static_lines[i])
      else:
        emit(goto(0,height-i),CLEAR_LINE, static_lines[i])
      gotoInput()
      flush()
  else:
    try:
      emit(goto(0,height-line),CLEAR_LINE,static_lines[line])
      gotoInput()
      flush()
    except IndexError as err:
      write([console.fg.red,err,console.fg.default])

def print(*args, **kwargs): # Patch the print function to use graph.write()
    return write(*args, **kwargs)

def init():
  global static_lines
  global constant_buffer
  global input_location
  global input_line
  emit(CLEAR,goto(0,0),SAVE_CURSOR)
  flush()
  __builtin__.print = write
  static_lines=[]
  constant_buffer=[]

  input_location = [0,0]
  input_line = 0

# emit saves stuff to the buffer
# buffer is a bunch of bytes which get ran at the next print statement
# print(text, flush=True) prints the text and then prints the buffer
# print(text) prints the buffer and then the text
# sys.stdout.flush() prints the buffer
# buffer clears on print
