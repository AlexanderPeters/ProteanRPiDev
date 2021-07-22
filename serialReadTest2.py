import time
import struct
from pySerialTransfer import pySerialTransfer

if __name__ == '__main__':
  try:
    link = pySerialTransfer.SerialTransfer('serial0')

    link.open()
    time.sleep(2) # allow some time for the Arduino to completely reset
    print('Starting')

    while True:
      time.sleep(1)

      while not link.available():
        if link.status < 0:
          print('ERROR: {}'.format(link.status))
        else:
          print('.',end='',flush=True)
        time.sleep(0.25)
      print()

      response = link.rxBuff[:link.bytesRead]
      binary_str = bytearray(response)
      print(binary_str)

      #unpacked_resp = struct.unpack('iiii', binary_str)
      #print('RCVD: %s' % str(unpacked_resp))

      print(' ')

  except KeyboardInterrupt:
    link.close()

