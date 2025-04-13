import requests
from flask import Flask, request, jsonify, Response
from twilio.twiml.voice_response import VoiceResponse, Start
import os
import assemblyai as aai
from twilio.rest import Client
from flask_cors import CORS
# ========== CONFIGURATION ==========
client = Client("ACfa697543259291e2cc7c9959528b2e39", "78763e2424d044957294a83f191ef0b3")
CALLBACK_BASE_URL = "https://e7b7-171-48-110-91.ngrok-free.app"
WS_SERVER_URL = "wss://four-jars-sort.loca.lt/media-stream"

app = Flask(__name__)
CORS(app,origins=['*'])
active_calls = {}

ASSEMBLYAI_API_KEY = "5750c96c9f154e4cb6152b1bd1eba3fd"  # Replace with your AssemblyAI API key

aai.settings.api_key = ASSEMBLYAI_API_KEY

transcriber = aai.Transcriber()


call_status_current = "Checking"
global_transcript = ""
# ========== FLASK ROUTES ==========

@app.route("/start-call", methods=["POST"])
def start_call():
    data = request.json
    to_number = data.get("to")

    if not to_number:
        return jsonify({"error": "Missing 'to' number"}), 400

    try:
        call = client.calls.create(
            to=to_number,
            from_="+19412057703",
            url=f"{CALLBACK_BASE_URL}/voice",
            record=True,
            recording_status_callback=f"{CALLBACK_BASE_URL}/recording-status",
            recording_status_callback_method="POST",
            status_callback=f"{CALLBACK_BASE_URL}/call-status",
            status_callback_event=["initiated", "ringing", "answered", "completed"],
            status_callback_method="POST"
        )

        active_calls[call.sid] = {
            "status": "in_progress",
            "start_time": None,
            "hold_time": 0,
            "dead_air_time": 0,
            "call_sid": call.sid
        }

        return jsonify({"message": "Call started", "sid": call.sid})

    except Exception as e:
        print("[ERROR] Failed to start call:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/end-call", methods=["POST"])
def end_call():
    sid = request.json.get("sid")

    if not sid:
        return jsonify({"error": "Missing 'sid'"}), 400

    try:
        client.calls(sid).update(status="completed")
        return jsonify({"message": "Call ended"})
    except Exception as e:
        print("[ERROR] Failed to end call:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/recording-status", methods=["POST"])
def recording_status():
    recording_url = request.form.get("RecordingUrl")
    call_sid = request.form.get("CallSid")
    duration = request.form.get("RecordingDuration")

    print(f"[RECORDING COMPLETE] Call SID: {call_sid}")
    print(f"Recording URL: {recording_url}.mp3")
    print(f"Duration: {duration} seconds")

    transcript = transcribe_recording(f"{recording_url}.mp3")
    if transcript:
        print(f"[FINAL TRANSCRIPT] {transcript}")

    return Response("OK", status=200)


@app.route("/send-whatsapp", methods=["POST"])
def send_whatsapp():
    data = request.json
    to = data.get("to")
    body = data.get("message")
    account_sid = 'ACfa697543259291e2cc7c9959528b2e39'
    auth_token = '78763e2424d044957294a83f191ef0b3'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
      from_='whatsapp:+14155238886',
      body=body,
      to=f'whatsapp:{to}'
    )

    print(message.sid)
    return jsonify({"success": True, "sid": message.sid}), 200
    

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()  
    start = Start()
    start.stream(name="call-audio", url=WS_SERVER_URL)
    response.append(start)
    response.say("You are connected. This call will be recorded and transcribed. We are testing Elite support for testing our project . Thank you for your pateince")
    return Response(str(response), mimetype="text/xml")

@app.route("/call-status", methods=["GET"])
def get_call_status():
    global call_status_current
    global global_transcript
    return jsonify({"status":call_status_current,"transcript":global_transcript}), 200
    
    
@app.route("/call-status", methods=["POST"])
def call_status():
    status = request.form.get("CallStatus")
    sid = request.form.get("CallSid")
    from_number = request.form.get("From")
    to_number = request.form.get("To")
    global call_status_current
    call_status_current = status
    print(f"[CALL STATUS] SID: {sid} | From: {from_number} | To: {to_number} | Status: {call_status_current}")
    return Response("OK", status=200)


# ========== TRANSCRIPTION UTILITY ==========


import tempfile


def transcribe_recording(recording_url):
    try:
        # Download the audio from Twilio
        audio_file_path = download_audio_from_twilio(recording_url)
        if not audio_file_path:
            print("[ERROR] Failed to download audio from Twilio")
            return None
        # Upload the downloaded file to AssemblyAI using SDK
        transcript = transcriber.transcribe(audio_file_path)
        print(transcript.text)
        global global_transcript
        global_transcript = transcript.text
        return transcript.text

    except Exception as e:
        print("[ERROR] Transcription failed:", e)
        return None

def download_audio_from_twilio(recording_url):
    try:
        print(f"[INFO] Downloading audio from Twilio: {recording_url}")
        response = requests.get(recording_url)

        if response.status_code == 200:
            # Use tempfile to create a safe temp file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                audio_file_path = temp_file.name  # Path to the temp file
                print(f"[INFO] Audio downloaded successfully to {audio_file_path}")
            return audio_file_path
        else:
            print(f"[ERROR] Failed to download audio: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Failed to download audio: {e}")
        return None


# ========== ENTRY POINT ==========

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
