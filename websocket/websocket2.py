import asyncio
import websockets
import json

def callWebSocket (uri, message):
	asyncio.get_event_loop().run_until_complete(
		sendSocketMessage(uri, message))

async def sendSocketMessage(uri, message):
    async with websockets.connect(uri) as websocket:
        data = {"message": message}
        await websocket.send(json.dumps(data))
        await websocket.recv()

# This is how you will have to encode the images to sent them back after creating the new satellite
# import base64
# encoded_string = base64.b64encode(image_file.read())

callWebSocket("ws://fierce-dawn-73363.herokuapp.com", "der base64 code von deinem image ")