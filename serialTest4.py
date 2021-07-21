from time import sleep
from pySerialTransfer import pySerialTransfer as txfer
import numpy as np
import re
import RPi.GPIO as GPIO

port = 'serial0'
hwResetPin = 26 # GPIO pin 26 not physical pin 26

def sendMessage(message):
    for index in range(len(message)):
        link.txBuff[index] = message[index]
    link.send(len(message))

def ping():
    alive = ['A','L','I','V','E','?']
    sendMessage(alive)

def getResponse(): # Returns false if no message is available
    if link.available():
        if link.status >= 0:
            response = ''
            for index in range(link.bytesRead):
                char = chr(link.rxBuff[index])
                response += char

            return response.rstrip('\x00') # Fix shit, strings be damned
        else:
            print('Error: {}'.format(link.status))
            return 'False'
    else:
        return 'False'     

def init():
    GPIO.setmode(GPIO.BCM) # Setup GPIO for Arduino HW reset
    GPIO.setup(hwResetPin, GPIO.OUT)

    global link
    link = txfer.SerialTransfer(port)    
    link.open()
    sleep(5) # Allow time for arduino to reset

def negotiateConnection(): # Attempts to establish a connection with the arduino
    attempts = 1
    while True:
        print('Attempting Connection: ' + str(attempts))
        ping()
        response = getResponse()

        if response == 'ALIVE':
            break
        else:
            if attempts >= 10:
                print('Arduino not found after 10 connection attempts')
                attempts = 0
                resetArduino()
                negotiateConnection()
                return None
            sleep(0.5)
            attempts += 1
    print('Connection established')

def getImage():
    takeImage = ['T','A','K','E','I','M','A','G','E']
    sendMessage(takeImage)
    sleep(0.1)
    return getResponse()

def resetArduino():
    print('Reseting Arduino')
    GPIO.output(hwResetPin, GPIO.HIGH)
    sleep(1) # 0.25s maybe ok?
    GPIO.output(hwResetPin, GPIO.LOW)
    sleep(5) # Allow time for Arduino to boot


if __name__ == '__main__':
    try:
        print('Starting Program')
        init()
        negotiateConnection()
        
        while True:
            image = getImage()
            if image and  image != 'False':
                print(image)
            else:
                print('No Image Found, Attempting to Renogotiate Connection')
                negotiateConnection()
            sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        link.close()

