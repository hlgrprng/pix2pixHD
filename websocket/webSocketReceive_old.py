import asyncio
import websockets
import json
import base64
import cv2
import numpy as np
from datetime import datetime
import os.path
from os import path

imageTestFolder = '../datasets/cityscapes/test_A/'

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

async def receiveWebsocket():
    uri = "ws://fierce-dawn-73363.herokuapp.com"
    async with websockets.connect(uri) as websocket:
        msgFromServer = await websocket.recv()
        parsedMsg = json.loads(msgFromServer)
        if 'image' in parsedMsg:
            img = readb64(parsedMsg['image'])
            imageName = datetime.now().strftime("%m%d%Y%H%M%S") + '-test.jpg'
            if (path.exists(imageTestFolder)):
                cv2.imwrite(imageTestFolder + '/' + imageName, img)
                print('Image received and saved')
                os.system("cd .. && python test.py --name cityscapes --label_nc 0 --no_instance")
            else:
                print('Wrong folder path: ', imageTestFolder)
        else:
            print('No image attribute in message', parsedMsg)

while True:
    asyncio.get_event_loop().run_until_complete(receiveWebsocket())
