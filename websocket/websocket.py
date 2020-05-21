import asyncio
import websockets
import json
import base64

async def hello():
    uri = "ws://fierce-dawn-73363.herokuapp.com"
    async with websockets.connect(uri) as websocket:
        msgFromServer = await websocket.recv()
        parsedMsg = json.loads(msgFromServer)
        parsedMsg = json.loads(parsedMsg)
        if 'image' in parsedMsg:
            parsedMsg['image'] = parsedMsg['image'].replace('data:image/png;base64,', '')
            image = base64.b64decode(parsedMsg['image'])
            print('Image received', parsedMsg['image'])
        else:
            print('No image attribute in message', parsedMsg)

while True:
    asyncio.get_event_loop().run_until_complete(hello())