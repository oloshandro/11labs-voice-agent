from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import threading
from datetime import datetime


class AgentController:
    def __init__(self, config, api_key, agent_id):
        self.api_key = api_key
        self.agent_id = agent_id
        self.log_dir = config.get('LOG_DIR')
        self.transcript_log = []

        self.client = ElevenLabs(api_key=self.api_key)
        self.conversation = None
        self.thread = None
        self.conversation_id = None

    def log_user_transcript(self, text):
        print(f"User: {text}")
        self.transcript_log.append(f"User: {text}")
    
    def log_agent_response(self, text):
        print(f"Agent: {text}")
        self.transcript_log.append(f"Agent: {text}")

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
            self.conversation.start_session()
            self.conversation_id = self.conversation.wait_for_session_end()
            print(f"\nConversation ended. ID: {self.conversation_id}")
            self.save_transcript()
            self.conversation = None

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
        print("Started agent thread")

    def stop(self):
        if self.conversation:
            try:
                self.conversation.end_session()
            except OSError as e:
                print(f"[⚠] Error while stopping session: {e}")
            self.conversation = None
            print("Stopped agent session")
