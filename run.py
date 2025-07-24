from app import create_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, use_reloader=False)



'''
# Load API key and agent ID from environment variables
api_key = os.getenv("ELEVENLABS_API_KEY")
agent_id = os.getenv("AGENT_ID")

if not api_key or not agent_id:
    raise ValueError("Please set ELEVENLABS_API_KEY and AGENT_ID as environment variables.")

# Store transcript lines
transcript_log = []

# Callbacks to log conversation
def log_user_transcript(text):
    print(f"User: {text}")
    transcript_log.append(f"User: {text}")

def log_agent_response(text):
    print(f"Agent: {text}")
    transcript_log.append(f"Agent: {text}")

def log_correction(original, corrected):
    print(f"Agent corrected: {original} -> {corrected}")
    transcript_log.append(f"Agent corrected: {original} -> {corrected}")

# Create the ElevenLabs client and conversation instance
client = ElevenLabs(api_key=api_key)

conversation = Conversation(
    client,
    agent_id,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_user_transcript=log_user_transcript,
    callback_agent_response=log_agent_response,
    callback_agent_response_correction=log_correction
)

# Graceful shutdown with Ctrl+C
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

# Start conversation
conversation.start_session()

# Wait for conversation to end
conversation_id = conversation.wait_for_session_end()
print(f"\nConversation ended. ID: {conversation_id}")

# Save transcript to file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"conversation_{timestamp}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("\n".join(transcript_log))

print(f"Transcript saved to {filename}")
'''