"""
Application configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-urbanflow-2024')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # WebSocket
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS
    SOCKETIO_LOGGER = DEBUG
    SOCKETIO_ENGINEIO_LOGGER = DEBUG
    
    # Database - PostgreSQL
    # Utilisez DATABASE_URL de l'environnement ou SQLite en fallback
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        # Fallback SQLite pour développement
        SQLALCHEMY_DATABASE_URI = 'sqlite:///urbanflow.db'
        print("⚠️  PostgreSQL non configuré, utilisation de SQLite")
    else:
        print("✅ Configuration PostgreSQL détectée")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    # Simulation
    SIMULATION_UPDATE_INTERVAL = 0.1  # seconds (100ms)
    MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'
    
    # Mock Simulation Settings
    MOCK_VEHICLE_COUNT = int(os.getenv('MOCK_VEHICLE_COUNT', '50'))
    MOCK_TRAFFIC_LIGHT_COUNT = int(os.getenv('MOCK_TRAFFIC_LIGHT_COUNT', '5'))
    MOCK_NETWORK_BOUNDS = {
        'min_lat': 48.85,
        'max_lat': 48.86,
        'min_lng': 2.35,
        'max_lng': 2.36,
    }
    
    # Network edges for mock simulation
    MOCK_NETWORK_EDGES = [
        {'id': 'edge_1', 'from': 'node_1', 'to': 'node_2', 'lanes': 2},
        {'id': 'edge_2', 'from': 'node_2', 'to': 'node_3', 'lanes': 2},
        {'id': 'edge_3', 'from': 'node_3', 'to': 'node_4', 'lanes': 2},
        {'id': 'edge_4', 'from': 'node_4', 'to': 'node_1', 'lanes': 2},
        {'id': 'edge_5', 'from': 'node_2', 'to': 'node_4', 'lanes': 1},
    ]