import asyncio
import websockets
import base64
import json
import io
from pydub import AudioSegment
from faster_whisper import WhisperModel

model = WhisperModel("C:/Users/rustg/Downloads/faster-whisper-base", local_files_only=True)



async def handle_connection(websocket, path):
    print("[WebSocket] Connection established")
    buffer = io.BytesIO()

    async for message in websocket:
        print("[WebSocket] Received message:", message)
        try:
            data = json.loads(message)

            if data.get("event") == "media":
                print("[WebSocket] Processing media data...")
                payload = data["media"]["payload"]
                audio_bytes = base64.b64decode(payload)

                # μ-law to PCM WAV (Twilio sends 8000Hz, 8-bit μ-law)
                ulaw_audio = AudioSegment(
                    audio_bytes,
                    sample_width=1,
                    frame_rate=8000,
                    channels=1
                )
                pcm_audio = ulaw_audio.set_sample_width(2).set_frame_rate(16000)
                buffer.write(pcm_audio.raw_data)

                if buffer.tell() > 32000:  # Enough for ~1 second
                    buffer.seek(0)
                    audio_chunk = buffer.read()
                    buffer = io.BytesIO()  # Reset for next chunk

                    try:
                        # Transcribe
                        print("[WebSocket] Attempting transcription...")
                        segments, _ = model.transcribe(audio_chunk, language="en", beam_size=1)
                        for segment in segments:
                            print(f"[TRANSCRIPT] {segment.text}")
                    except Exception as e:
                        print(f"[Error] Transcription failed: {e}")

            elif data.get("event") == "stop":
                print("[WebSocket] Stream ended")
                break
        except Exception as e:
            print(f"[Error] Error processing message: {e}")


async def main():
    print("[WebSocket Server] Listening on ws://0.0.0.0:5005/media-stream")
    async with websockets.serve(handle_connection, "0.0.0.0", 5005):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
