import asyncio
import websockets
import json
import base64
from pydub import AudioSegment

async def test_ws_connection():
    uri = "ws://localhost:5005/media-stream"  # Update with your WebSocket server URL

    # Connect to the WebSocket server
    async with websockets.connect(uri) as websocket:
        print("[Test] Connected to WebSocket server.")

        # Example test audio data (can be any valid 8-bit mu-law audio bytes)
        audio_bytes = b'\x8e\x8f\x8e\x8d\x8c\x8b\x8a\x89\x88\x87\x86\x85\x84\x83\x82\x81\x80'

        # Convert to base64
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        # Create the message to send (simulating a media event)
        message = {
            "event": "media",
            "media": {
                "payload": audio_base64
            }
        }

        # Send the message
        await websocket.send(json.dumps(message))
        print("[Test] Sent media message.")

        # Optionally, you can also send a 'stop' event after some time
        stop_message = {
            "event": "stop"
        }
        await websocket.send(json.dumps(stop_message))
        print("[Test] Sent stop event.")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_ws_connection())
