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
    
    # Initialize database
    try:
        db.init_app(app)
        print(f"✅ Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        print("⚠️  Using in-memory SQLite as fallback")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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
        db_type = "PostgreSQL" if "postgresql" in app.config['SQLALCHEMY_DATABASE_URI'] else "SQLite"
        return jsonify({
            'message': 'Urban Flow API',
            'version': '1.0.0',
            'status': 'operational',
            'database': db_type,
            'endpoints': {
                'api': '/api',
                'health': '/api/health',
                'version': '/api/version',
                'websocket': 'ws://localhost:5000/ws'
            }
        })
    
    @app.route('/api/health')
    def health():
        db_status = 'connected'
        try:
            db.session.execute('SELECT 1')
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return jsonify({
            'status': 'healthy',
            'timestamp': '2024-01-25T14:30:00Z',
            'services': {
                'database': db_status,
                'websocket': 'active',
                'simulation': 'ready'
            }
        })
    
    @app.route('/api/version')
    def version():
        db_type = "PostgreSQL" if "postgresql" in app.config['SQLALCHEMY_DATABASE_URI'] else "SQLite"
        return jsonify({
            'version': '1.0.0',
            'api': 'REST + WebSocket',
            'simulation': 'Mock Mode',
            'database': db_type,
            'author': 'Urban Flow Team'
        })
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            print("⚠️  Database operations may be limited")
    
    return app

# Create application instance
app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Urban Flow Backend")
    print("=" * 50)
    
    # Detect database type
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if "postgresql" in db_url:
        print("💾 Database: PostgreSQL")
        db_name = db_url.split('/')[-1]
        print(f"   Name: {db_name}")
    elif "sqlite" in db_url:
        print("💾 Database: SQLite")
        print(f"   File: {db_url.split('///')[-1] if '///' in db_url else ':memory:'}")
    
    print("📡 WebSocket: ws://localhost:5000/ws")
    print("🌐 REST API: http://localhost:5000/api")
    print("🔄 Mock Simulation: Active")
    print("=" * 50)
    
    socketio.run(app, 
                 debug=app.config['DEBUG'], 
                 host='0.0.0.0', 
                 port=5000, 
                 use_reloader=False)