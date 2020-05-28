import asyncio
from functools import partial

import websockets
import json
import base64
import cv2
import numpy as np
from datetime import datetime
import os
from os import path

imageTestFolder = 'datasets/cityscapes/test_A/'

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

async def receiveWebsocket():
    # for local testing
    # uri = 'ws://localhost:8080'
    uri = "ws://fierce-dawn-73363.herokuapp.com"
    async with websockets.connect(uri) as websocket:
        msgFromServer = await websocket.recv()
        try:
            parsedMsg = json.loads(msgFromServer)
            if 'image' in parsedMsg and 'cropTime' in parsedMsg and 'folderName' in parsedMsg:
                img = readb64(parsedMsg['image'])
                imageName = parsedMsg['cropTime'] + '.jpg'
                folderName = parsedMsg['folderName'] + '/'
                if (path.exists(imageTestFolder)):
                    if not (path.exists(imageTestFolder + folderName)):
                        os.mkdir(imageTestFolder + folderName)

                    cv2.imwrite(imageTestFolder + folderName + '/' + imageName, img)
                    print('Image received and saved')
                else:
                    print('Wrong folder path: ', imageTestFolder)
            elif 'imageDone' in parsedMsg and 'folderName' in parsedMsg:
                folderWithImages = imageTestFolder + parsedMsg['folderName'] + '/'
                #os.system("cd .. && python test.py --name cityscapes --label_nc 0 --no_instance")
            else:
                print('Could not find sufficient attributes', parsedMsg)
        except Exception as exc:
            print('That was not a valid geoJson sent by client: ', msgFromServer)

while True:
    asyncio.get_event_loop().run_until_complete(receiveWebsocket())
