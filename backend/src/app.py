"""
Main Flask application
"""
import os
import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import Config
from models.simulation import db
from websocket.handlers import register_socketio_handlers
from websocket.simulation_stream import SimulationStream
from simulation.mock_simulator import MockSimulator

# Extensions
socketio = SocketIO()
simulator = MockSimulator()
simulation_stream = None

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    socketio.init_app(app, 
                     cors_allowed_origins=app.config['CORS_ORIGINS'],
                     async_mode='eventlet')
    
    # Initialize simulator
    global simulator, simulation_stream
    simulator = MockSimulator()
    simulation_stream = SimulationStream(socketio, simulator)
    
    # Register WebSocket handlers
    register_socketio_handlers(socketio, simulator, simulation_stream)
    
    # Register API blueprints
    from api.routes.simulation import simulation_bp
    from api.routes.scenarios import scenarios_bp
    from api.routes.metrics import metrics_bp
    from api.routes.vehicles import vehicles_bp
    
    app.register_blueprint(simulation_bp, url_prefix='/api')
    app.register_blueprint(scenarios_bp, url_prefix='/api')
    app.register_blueprint(metrics_bp, url_prefix='/api')
    app.register_blueprint(vehicles_bp, url_prefix='/api')
    
    # Basic routes
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Urban Flow API',
            'version': '1.0.0',
            'status': 'operational',
            'endpoints': {
                'api': '/api',
                'health': '/api/health',
                'version': '/api/version',
                'websocket': 'ws://localhost:5000/ws'
            }
        })
    
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'timestamp': '2024-01-25T14:30:00Z',
            'services': {
                'database': 'connected',
                'websocket': 'active',
                'simulation': 'ready'
            }
        })
    
    @app.route('/api/version')
    def version():
        return jsonify({
            'version': '1.0.0',
            'api': 'REST + WebSocket',
            'simulation': 'Mock Mode',
            'author': 'Urban Flow Team'
        })
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Urban Flow Backend")
    print("=" * 50)
    print("📡 WebSocket: ws://localhost:5000/ws")
    print("🌐 REST API: http://localhost:5000/api")
    print("💾 Database: SQLite (development mode)")
    print("🔄 Mock Simulation: Active")
    print("=" * 50)
    
    socketio.run(app, 
                 debug=app.config['DEBUG'], 
                 host='0.0.0.0', 
                 port=5000, 
                 use_reloader=False)