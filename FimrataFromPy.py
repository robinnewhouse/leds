from pyfirmata import *
import time

SYSEX_START = 0xF0   
SYSEX_END = 0xF7
WRITE_LIGHTS = 0x01
BAUDRATE = 57600

i_pin = 5 #  Incoming Firmata data on this pin is handled specially.
r_pin = 6
g_pin = 7
b_pin = 8
render_pin = 9

board = Arduino('/dev/cu.usbmodem1602551')
board.digital[13].write(1)

it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[0].read()



data=[i_pin,0xff,0xff,0xff]


board.send_sysex(CAPABILITY_QUERY,[])
board.digital[13].write(0)
time.sleep(0.5)
board.digital[13].write(1)
time.sleep(0.5)
board.digital[13].write(0)
# time.sleep(0.5)
# board.digital[13].write(1)
# time.sleep(0.5)
# board.digital[13].write(0)
# time.sleep(0.5)
