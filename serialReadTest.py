#!/usr/bin/env python
import time
import serial
import atexit

ser = serial.Serial(
        # port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        port='dev/ttyAMA0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

def handle_cleanup():
    ser.close()
    print('\n')
    print('Serial Port Closed and Program Exiting')

def main():
    while 1:
        x = ser.readline()
        print(x)

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        handle_cleanup()
