from time import sleep
import numpy as np
from pprint import pprint
from dataclasses import dataclass
from pySerialTransfer import pySerialTransfer as txfer
from PIL import Image


imgSize = (800, 600) #SVGA W x H

packetCounter = 1
bufferPointer = 0
tempImageBuffer = [0] * 32000
def copyToImageBuff(dataLength):
    print('Attempting to copy image buffer')
    global bufferPointer
    global packetCounter

    for y in range(dataLength):
        tempImageBuffer[bufferPointer + y] = txfer.rxBuff[y + len(ImgMetaData)]

    bufferPointer += dataLength
    packetCounter += 1 
    print(len(tempImageBuffer))

@dataclass
class ImgMetaData:
    counter: int
    imSize: int
    numLoops: int
    sizeLastLoop: int


metaData = ImgMetaData(None, None, None, None)
def main():
    global bufferPointer
    global packetCounter

    try:
        # link = txfer.SerialTransfer('/dev/ttyS0')
        # link = txfer.SerialTransfer('/dev/ttyAMA0')
        link = txfer.SerialTransfer('serial0')
        link.open()
        print('Searching for link')
        sleep(5) # allow some time for the Arduino to completely reset
        
        while True:
            #print('Starting search for link')
            ###################################################################
            # Wait for a response and report any errors while receiving packets
            ###################################################################
            while not link.available():
                link.txBuff[0] = 'h'
                link.txBuff[1] = 'i'

                link.send(2)

                sent = ''
                for y in range(len(link.txBuff)):
                    sent += link.txBuff[y]
                print('Sent: ' + sent)

                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))
               # pprint(vars(link))
               # print(dir())
               # print(globals())
               # print(locals())
               # print(vars(link))
               # print(len(link.rxBuff))
               # print(link.payIndex)
                sleep(0.1)

            print('Link Found!')

            txfer.rxObj(metaData, len(metaData))
            print(metaData)
            if metaData.counter == 1:  
                copyToImageBuff(txfer.MAX_PACKET_SIZE - len(metaData))
            elif metaData.counter==packetCounter:
                if packetCounter < metaData.numLoops:        
                    copyToImageBuff(txfer.MAX_PACKET_SIZE - len(metaData))
                elif metaData.counter == packetCounter:
                    copyToImageBuff(metaData.sizeLastLoop)     
                
                if packetCounter > metaData.numLoops:
                    img = Image.fromstring('RGB', imgSize, tempImageBuffer, 'raw', 'F;16')
                    img.save('testImage.jpeg')

                    packetCounter = 1
                    bufferPointer = 0
    
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass

if __name__ == '__main__':
    main()
    
