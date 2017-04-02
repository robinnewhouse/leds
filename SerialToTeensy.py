import time
import serial

# import binascii
NUM_LEDS = 100
read_delay = 0.01  # remove
render_delay = 0.01  # how long to wait between frames
fps = 2000  # alternatively define frames per second
render_delay = 1 / fps
wait_for_confirmation_delay = 0.001  # how long to wait between successive tries for confirmation
light_run_time = 10  # how long should the program run?
header = [0xDE, 0xAD, 0xBE, 0xEF]
recieve_confirmed = b'*'  # should be the same on the arduino

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port="/dev/cu.usbmodem1602551",
    baudrate=9600,
    timeout=0.5
    # parity=serial.PARITY_ODD,
    # stopbits=serial.STOPBITS_TWO,
    # bytesize=serial.SEVENBITS
)

"""
Scale the given value from the scale of src to the scale of dst.
"""


def scale(val, src, dst):
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def test_serial_hex():
    print(ser.name)  # check which port was really used
    # ser.write([0xDE, 0xAD, 0xBE, 0xEF])
    ser.write(
        [0xDE, 0xAD, 0xBE, 0xEF, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00,
         0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F, 0xFF, 0x00, 0x1F])

    # for x in range(0,NUM_LEDS):
    #     ser.write([0xFF, 0x00, 0x1F])

    ser.write([244, 244, 244])

    start_time = time.time()
    while time.time() < start_time + read_delay:
        try:
            # bin_val = int(ser.readline())
            print(ser.readline().decode("ascii"), end=" ", flush=True)
        except Exception as e:
            break
    print()


def test_serial_string():
    print(ser.name)  # check which port was really used
    ser.write(b'fuck')

    start_time = time.time()
    while time.time() < start_time + read_delay:
        try:
            int_val = int(ser.readline())
            print(chr(int_val), end='', flush=True)
        except Exception as e:
            pass
    print()


leds = [None] * NUM_LEDS


def cycle_trough_rainbow():
    start_time = time.time()
    direction = [1, 1, 1]
    color = [0, 0, 0]
    frame = 0
    while time.time() < start_time + light_run_time:

        color[0] = color[0] + 5 * direction[0]
        color[1] = color[1] + 1 * direction[1]
        color[2] = color[2] + 2 * direction[2]
        for i in range(len(color)):
            if color[i] >= 255:
                color[i] = 255
                direction[i] = -1
            if color[i] <= 0:
                color[i] = 0
                direction[i] = 1

        for i in range(0, NUM_LEDS):
            leds[i] = color
        send_leds_to_serial(leds)
        frame = frame + 1
        if frame % 100 == 0:
            fps(frame, start_time)


def fps(frames, start_time):
    print("fps: ", "{0:.2f}".format(frames / (time.time() - start_time)))
    pass


def bounce():
    start_time = time.time()
    direction = 1
    position = 0
    color = [100, 0, 150]
    while time.time() < start_time + light_run_time:
        if position >= NUM_LEDS - 1:
            direction = -1
        if position <= 0:
            direction = 1
        leds = [[0, 0, 0]] * NUM_LEDS
        leds[position] = color
        position += direction
        send_leds_to_serial(leds)


def send_leds_to_serial(leds):
    color_array = [None] * NUM_LEDS * 3
    for i in range(0, NUM_LEDS):
        color_array[i * 3 + 0] = leds[i][0]  # r
        color_array[i * 3 + 1] = leds[i][1]  # g
        color_array[i * 3 + 2] = leds[i][2]  # b
    ser.write(header + color_array)
    time.sleep(render_delay)
    while (not get_confirmation()):
        time.sleep(wait_for_confirmation_delay)


def get_confirmation():
    start_time = time.time()
    while time.time() < start_time + 2:
        try:
            response = ser.readline()
            # time.sleep(0.01)
            # print(response,end=' ',flush=True)
            if (recieve_confirmed in response):
                return True
            else:
                return False
        except Exception as e:
            print("excepted")

    return response == recieve_confirmed


# while True:
#     print("reading")
#     print(ser.readline())

def main():
    # test_serial_hex()
    cycle_trough_rainbow()
    # bounce()
    # print(ser.isOpen())

    # print(ser.read())

    # ser.write([0xFF, 0xFF, 0xFF])

    ser.close()  # close port


if __name__ == '__main__':
    main()
