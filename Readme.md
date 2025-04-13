Sure! Here's a clean and detailed `README.md` for your Flask-based Call System Backend using Twilio and AssemblyAI:

---

# 📞 Call System Backend

This is a Flask backend for a voice call and transcription system using **Twilio** for call management and **AssemblyAI** for transcription. It supports real-time audio streaming, automatic recording, transcription, call analytics, and WhatsApp notifications.

---

## 🚀 Features

- Start and end voice calls via Twilio
- Real-time call audio streaming over WebSockets
- Automatic transcription using AssemblyAI
- Call status tracking (`initiated`, `ringing`, `answered`, `completed`)
- WhatsApp messaging via Twilio
- Recording download and transcription after call ends
- Basic analytics: hold time, dead air time, call duration
- CORS enabled for frontend integration

---

## ⚙️ Tech Stack

- **Python** + **Flask**
- **Twilio** (Voice, WhatsApp, Media Streams)
- **AssemblyAI** (Transcription)
- **WebSockets**
- **REST API**

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/call-system-backend.git
cd call-system-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

You’ll need:
- Flask
- requests
- twilio
- assemblyai
- flask_cors

### 3. Set Environment Variables (Optional but recommended)

Instead of hardcoding, set the following:

```bash
export TWILIO_ACCOUNT_SID=your_twilio_sid
export TWILIO_AUTH_TOKEN=your_twilio_auth
export ASSEMBLYAI_API_KEY=your_assemblyai_key
```

Or set them inside a `.env` file and load using `python-dotenv`.

### 4. Run the Server

```bash
python app.py
```

---

## 🔧 API Endpoints

### Start a Call

```http
POST /start-call
```

**Body:**
```json
{ "to": "+1234567890" }
```

---

### End a Call

```http
POST /end-call
```

**Body:**
```json
{ "sid": "CAxxxxxxxxxxxxxxxx" }
```

---

### Call Voice Webhook

```http
POST /voice
```

> Twilio calls this URL to handle the call with TwiML (starts streaming & plays message)

---

### Call Status Callback

```http
POST /call-status
```

> Receives live call status updates

---

### Get Current Call Status

```http
GET /call-status
```

Returns:
```json
{ "status": "in-progress", "transcript": "..." }
```

---

### Recording Status Callback

```http
POST /recording-status
```

> Triggered when recording is complete. Automatically transcribes and stores the result via an external API.

---

### Get Transcript from URL

```http
GET /get-transcript?url=https://.../audio.mp3
```

Returns:
```json
{ "transcript": "Hello, this is a test call..." }
```

---

### Get Call Details

```http
GET /call-details?sid=CAxxxxxxxx
```

Returns:
```json
{
  "sid": "CA...",
  "status": "completed",
  "hold_time": 0,
  "dead_air_time": 0,
  "start_time": 1712951837.2871
}
```

---

### Send WhatsApp Message

```http
POST /send-whatsapp
```

**Body:**
```json
{
  "to": "+1234567890",
  "message": "Hello from Elite support!"
}
```

---

## 🧠 How It Works

1. **Call Initiation**: A call is started via Twilio's API.
2. **Voice Webhook**: On answer, Twilio streams audio to a WebSocket and plays a message.
3. **Recording**: After the call ends, Twilio uploads a recording.
4. **Transcription**: Recording is downloaded and transcribed using AssemblyAI.
5. **Analytics**: Status, duration, and transcription are stored.
6. **WhatsApp**: Optional WhatsApp messages can be triggered.

---

## 📦 External Integrations

- [Twilio Voice](https://www.twilio.com/docs/voice)
- [Twilio WhatsApp](https://www.twilio.com/docs/whatsapp)
- [Twilio Media Streams](https://www.twilio.com/docs/voice/twiml/stream)
- [AssemblyAI](https://www.assemblyai.com/)

---

## 📁 File Structure

```
call-system-backend/
├── app.py                   # Main Flask server
├── requirements.txt         # Dependencies
└── README.md                # Project docs
```

---

## 📬 Contact

For issues or contributions, feel free to open a PR or reach out!

---

Would you like me to auto-generate the `requirements.txt` too?
