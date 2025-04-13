# websocket_server.py
import asyncio
import websockets

async def media_handler(websocket):
    async for message in websocket:
        # Process the audio stream here
        print("Received:", message[:50])  # Placeholder
        # Add logic to detect dead air or hold time

start_server = websockets.serve(media_handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
