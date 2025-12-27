from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .websocket.handlers import handle_connect, handle_disconnect, handle_command
from .simulation.mock_simulator import MockSimulator
from .websocket.simulation_stream import SimulationStream

app = Flask(__name__)
app.config.from_object(Config)

# Extensions
CORS(app)
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Simulation
simulator = MockSimulator()
simulation_stream = SimulationStream(socketio, simulator)

# WebSocket events
@socketio.on('connect')
def on_connect():
    handle_connect()

@socketio.on('disconnect')
def on_disconnect():
    handle_disconnect()

@socketio.on('command')
def on_command(data):
    handle_command(data)

# API Routes
from .api.routes.simulation import simulation_bp
from .api.routes.scenarios import scenarios_bp
from .api.routes.metrics import metrics_bp

app.register_blueprint(simulation_bp, url_prefix='/api')
app.register_blueprint(scenarios_bp, url_prefix='/api')
app.register_blueprint(metrics_bp, url_prefix='/api')

@app.route('/')
def index():
    return {'message': 'Urban Flow API', 'version': '1.0.0'}

if __name__ == '__main__':
    print("🚀 Urban Flow Backend starting...")
    print("📡 WebSocket: ws://localhost:5000/ws")
    print("🌐 REST API: http://localhost:5000/api")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)