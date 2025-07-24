# ElevenLabs Voice Agent (Flask App)

A local voice assistant built using the ElevenLabs Conversational AI SDK. This project runs an agent with system audio (mic & speakers) and provides a simple web interface for starting/stopping the conversation and viewing agent status.

---

## Features

- Real-time voice interaction using `DefaultAudioInterface`
- ElevenLabs Conversational Agent API integration
- Flask-based web UI with `Start` and `Stop` buttons
- Transcript saving with conversation ID in filenames
- Background thread for non-blocking interaction

---

## Setup

1. Clone the repo
2. Create `.env` file:

ELEVENLABS_API_KEY=your_api_key_here

AGENT_ID=your_agent_id_here


3. Install dependencies:

```pip install -r requirements.txt```

4. Run the app:

```python run.py```


## Transcripts are automatically saved to:

```app/chat_logs/conversation_YYYYMMDD_HHMMSS_<conversation_id>.txt```

Each file contains alternating user/agent lines.


