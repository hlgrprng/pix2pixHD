import asyncio
import websockets
import json
from PIL import Image
import base64
from io import BytesIO

def getBase64FromImageNumpy(image_numpy):
    image_pil = Image.fromarray(image_numpy)
    buffered = BytesIO()
    image_pil.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())

def formatBase64AndCallWebSocket(uri, messageType, image_numpy):
    img_str = getBase64FromImageNumpy(image_numpy)
    callWebSocket(uri, messageType, img_str)

# Packing JSON with {messageType: message}

def callWebSocket (uri, messageType, message):
    asyncio.get_event_loop().run_until_complete(
		sendSocketMessage(uri, messageType, message))

async def sendSocketMessage(uri, messageType, message):
    async with websockets.connect(uri) as websocket:
        data = {messageType: message}
        await websocket.send(json.dumps(data))

# Sending complete JSON

def callWebSocketJson (uri, data):
	asyncio.get_event_loop().run_until_complete(
		sendJsonSocketMessage(uri, data))

async def sendJsonSocketMessage(uri, data):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(data))

# This is how you will have to encode the images to sent them back after creating the new satellite
# import base64
# encoded_string = base64.b64encode(image_file.read())

# callWebSocket("ws://fierce-dawn-73363.herokuapp.com", "der base64 code von deinem image ")