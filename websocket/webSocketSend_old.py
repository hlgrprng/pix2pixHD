import asyncio
import websockets
import json

import numpy as np
from PIL import Image
import base64
from io import BytesIO

def formatBase64AndCallWebSocket(uri, image_numpy):
    image_pil = Image.fromarray(image_numpy)
    buffered = BytesIO()
    image_pil.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    print(img_str)
    callWebSocket(uri, img_str)
    print('Image sent')

def callWebSocket(uri, img_str):
	asyncio.get_event_loop().run_until_complete(
		sendSocketMessage(uri, img_str))

async def sendSocketMessage(uri, img_str):
    async with websockets.connect(uri) as websocket:
        data = {"message": str(img_str)}
        datasend = json.dumps(data)
        try:
            await websocket.send(datasend)
            await websocket.recv()
        except Exception:
            print('error')
            exit(1)
