from flask import Flask
from flask_socketio import SocketIO
from app.routes.routes import register_routes
from app.services.agent_controller import AgentController
from dotenv import load_dotenv
import os
load_dotenv()

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config.py')
    app.config.from_pyfile(configuration)

    api_key = os.getenv("ELEVENLABS_API_KEY")
    agent_id = os.getenv("AGENT_ID")

    if not api_key or not agent_id:
        raise ValueError("Please set ELEVENLABS_API_KEY and AGENT_ID as environment variables.")

    app.agent_controller = AgentController(app.config, api_key, agent_id, socketio)

    register_routes(app)
    socketio.init_app(app)

    return app
