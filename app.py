from flask import Flask, request, jsonify, Response
from twilio.twiml.voice_response import VoiceResponse, Start, Stream
from twilio_config import client, TWILIO_PHONE_NUMBER
import uuid

app = Flask(__name__)

active_calls = {}

@app.route("/start-call", methods=["POST"])
def start_call():
    data = request.json
    to_number = data["to"]
    call_sid = str(uuid.uuid4())

    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE_NUMBER,
        url="https://01ba-171-48-110-117.ngrok-free.app/voice",
        record=True,  # <--- Record the full call
        recording_status_callback="https://01ba-171-48-110-117.ngrok-free.app/recording-status",  # Optional: get the URL
        recording_status_callback_method="POST",# Replace with your ngrok
        status_callback="https://01ba-171-48-110-117.ngrok-free.app/call-status",
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


@app.route("/end-call", methods=["POST"])
def end_call():
    data = request.json
    sid = data["sid"]
    call = client.calls(sid).update(status="completed")
    return jsonify({"message": "Call ended"})

@app.route("/recording-status", methods=["POST"])
def recording_status():
    recording_url = request.form.get("RecordingUrl")
    call_sid = request.form.get("CallSid")
    duration = request.form.get("RecordingDuration")

    print(f"[RECORDING COMPLETE] Call SID: {call_sid}")
    print(f"Recording URL: {recording_url}.mp3")
    print(f"Duration: {duration} seconds")

    # You could save this in a DB or send to frontend
    return Response("OK", status=200)



@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    start = Start()
    start.stream(name="call-audio", url="wss://01ba-171-48-110-117.ngrok-free.app/media-stream")
    response.append(start)
    response.say("You are connected. This call will be recorded and transcribed.")
    return Response(str(response), mimetype="text/xml")


@app.route("/status-callback", methods=["POST"])
def status_callback():
    # Called by Twilio when call status changes (optional)
    print(request.form)
    return "", 204


@app.route("/call-status", methods=["POST"])
def call_status():
    status = request.form.get("CallStatus")
    sid = request.form.get("CallSid")
    from_number = request.form.get("From")
    to_number = request.form.get("To")

    print(f"[CALL STATUS] SID: {sid} | From: {from_number} | To: {to_number} | Status: {status}")
    return Response("OK", status=200)


if __name__ == "__main__":
    app.run(debug=True)
