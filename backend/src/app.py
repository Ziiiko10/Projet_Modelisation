import time
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from .config import Config
from .simulation.simulator import MockSimulator
from .websocket.simulation_stream import SimulationStream
from .websocket.handlers import setup_socket_handlers
from .api.routes import setup_api_routes

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialisation de l'application
app = Flask(__name__)
app.config.from_object(Config)

# Extensions
CORS(app, origins=app.config['CORS_ORIGINS'])
socketio = SocketIO(
    app,
    cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS'],
    async_mode=app.config['SOCKETIO_ASYNC_MODE'],
    logger=app.config['DEBUG'],
    engineio_logger=app.config['DEBUG']
)

# Initialisation des composants
simulator = MockSimulator()
simulation_stream = SimulationStream(socketio, simulator)

# ========== ROUTES API DE BASE ==========

@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({
        'name': 'Urban Flow API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'api': '/api/*',
            'websocket': 'ws://localhost:5000',
            'documentation': '/api/docs'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de la santé de l'application"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'components': {
            'database': 'connected' if app.config.get('DATABASE_URL') else 'not_configured',
            'websocket': 'running',
            'simulator': 'running' if simulator.is_running else 'stopped',
            'streaming': 'active' if simulation_stream.streaming else 'inactive'
        }
    })

@app.route('/api/version', methods=['GET'])
def version():
    """Version de l'API"""
    return jsonify({
        'name': 'Urban Flow',
        'version': '1.0.0',
        'api_version': 'v1',
        'mock_mode': app.config['MOCK_MODE'],
        'simulation_interval': app.config['SIMULATION_UPDATE_INTERVAL']
    })

# ========== SETUP DES HANDLERS ==========

# Setup WebSocket handlers
setup_socket_handlers(socketio, simulator, simulation_stream)

# Setup API routes
api_blueprint = setup_api_routes(simulator, simulation_stream)
app.register_blueprint(api_blueprint, url_prefix='/api')

# ========== GESTION DES ERREURS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ========== SHUTDOWN ==========

@app.teardown_appcontext
def shutdown(exception=None):
    """Nettoyage à la fermeture de l'application"""
    logger.info("Nettoyage de l'application...")
    if simulation_stream:
        simulation_stream.stop_streaming()
    if simulator:
        simulator.cleanup()

# ========== POINT D'ENTRÉE ==========

if __name__ == '__main__':
    from datetime import datetime
    
    print("=" * 60)
    print(f"🚀 Urban Flow Backend - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"📡 WebSocket: ws://localhost:5000")
    print(f"🌐 REST API: http://localhost:5000")
    print(f"🔧 Mode: {'Développement' if app.config['DEBUG'] else 'Production'}")
    print(f"🎮 Simulation: {'Mock' if app.config['MOCK_MODE'] else 'SUMO'}")
    print(f"⏱️  Intervalle: {app.config['SIMULATION_UPDATE_INTERVAL']*1000}ms")
    print("=" * 60)
    
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000,
        use_reloader=True,
        log_output=app.config['DEBUG']
    )