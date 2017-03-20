import time
import serial
import binascii
NUM_LEDS = 10
delay = 2
light_run_time = 10
header = [0xDE, 0xAD, 0xBE, 0xEF]
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port="/dev/cu.usbmodem1602551",
	baudrate=57600,
	timeout=1
	# parity=serial.PARITY_ODD,
	# stopbits=serial.STOPBITS_TWO,
	# bytesize=serial.SEVENBITS
)

"""
Scale the given value from the scale of src to the scale of dst.
"""
def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def test_serial_hex():
	print(ser.name)         # check which port was really used
	# ser.write([0xDE, 0xAD, 0xBE, 0xEF])
	ser.write([0xDE, 0xAD, 0xBE, 0xEF, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F])

	# for x in range(0,NUM_LEDS):
	# 	ser.write([0xFF, 0x00, 0x1F])

	ser.write([244, 244, 244])

	start_time = time.time()
	while time.time() < start_time+delay:
		try:
			# bin_val = int(ser.readline())
			print(ser.readline().decode("ascii"),end=' ',flush=True)
		except Exception as e: break
	print()

def test_serial_string():
	print(ser.name)         # check which port was really used
	ser.write(b'fuck')

	start_time = time.time()
	while time.time() < start_time+delay:
		try:
			int_val = int(ser.readline())
			print(chr(int_val),end='',flush=True)
		except Exception as e: pass
	print()

leds = [None]*NUM_LEDS
def cycle_trough_rainbow():
	start_time = time.time()
	direction = [1,1,1]
	color = [0,0,0]
	while time.time() < start_time+light_run_time:

		color[0] = direction[0 + 5]
		for i in range(0,NUM_LEDS):
			leds[i] = color
		send_leds_to_serial(leds)




def send_leds_to_serial(leds):
	color_array = [None]*NUM_LEDS*3
	for i in range(0,NUM_LEDS):
		color_array[i*3+0] = leds[i][0] #r
		color_array[i*3+1] = leds[i][1] #g
		color_array[i*3+2] = leds[i][2] #b
	ser.write(header + color_array)
	time.sleep(0.005)

def get_confirmation():
	start_time = time.time()
	while time.time() < start_time+delay:
		try:
			response = ser.readline()
			print(response,end=' ',flush=True)
			if(response == b'!'):
				return True
			
		except Exception as e: pass
	print()
	return response == b'!'

# test_serial_hex()
cycle_trough_rainbow()

# print(ser.isOpen())

# print(ser.read())

# ser.write([0xFF, 0xFF, 0xFF])


ser.close()             # close port
