from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import threading
import time
from datetime import datetime


class AgentController:
    def __init__(self, config, api_key, agent_id, socketio):
        self.api_key = api_key
        self.agent_id = agent_id
        self.log_dir = config.get('LOG_DIR')
        self.transcript_log = []
        self.socketio = socketio
        self.is_running = False

        self.client = ElevenLabs(api_key=self.api_key)
        self.conversation = None
        self.thread = None
        self.conversation_id = None

    def log_user_transcript(self, text):
        print(f"User: {text}")
        message = f"User: {text}"
        self.transcript_log.append(message)
        # Emit WebSocket event immediately (user finished speaking)
        self.socketio.emit('transcript_update', {
            'type': 'user',
            'text': text,
            'message': message
        })

    def log_agent_response(self, text):
        print(f"Agent: {text}")
        message = f"Agent: {text}"
        self.transcript_log.append(message)

        # Calculate estimated audio duration based on text length
        # Average speaking rate: ~15 characters per second
        estimated_duration = len(text) / 15.0

        # Emit after a delay to simulate audio playback timing
        def delayed_emit():
            time.sleep(estimated_duration)
            self.socketio.emit('transcript_update', {
                'type': 'agent',
                'text': text,
                'message': message
            })

        # Run in a separate thread to not block the callback
        threading.Thread(target=delayed_emit, daemon=True).start()

    def log_correction(self, original, corrected):
        print(f"Agent corrected: {original} -> {corrected}")

    def save_transcript(self):
        if not self.transcript_log:
            print("No transcript to save.")
            return     
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"{self.log_dir}/_{timestamp}_{self.conversation_id}.txt"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(self.transcript_log))
        print(f"[✔] Transcript saved to {filepath}")


    def start(self):
        if self.conversation:
            print("Conversation already running.")
            return

        self.transcript_log = []
        self.is_running = True

        self.conversation = Conversation(
            self.client,
            self.agent_id,
            requires_auth=True,
            audio_interface=DefaultAudioInterface(),
            callback_user_transcript=self.log_user_transcript,
            callback_agent_response=self.log_agent_response,
            callback_agent_response_correction=self.log_correction
        )

        def run():
            try:
                self.conversation.start_session()
                self.conversation_id = self.conversation.wait_for_session_end()
                print(f"\nConversation ended. ID: {self.conversation_id}")
                self.save_transcript()
            except Exception as e:
                print(f"[⚠] Conversation error: {e}")
            finally:
                self.conversation = None
                self.is_running = False

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        print("Started agent thread")

    def stop(self):
        if self.conversation:
            try:
                print("Stopping conversation...")
                self.conversation.end_session()
                # Save transcript before clearing
                if self.conversation_id:
                    self.save_transcript()
            except Exception as e:
                print(f"[⚠] Error while stopping session: {e}")
            finally:
                self.conversation = None
                self.is_running = False
            print("Stopped agent session")
