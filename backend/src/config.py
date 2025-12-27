import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-urbanflow')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # WebSocket
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///urbanflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Simulation
    SIMULATION_UPDATE_INTERVAL = 0.1  # secondes (100ms)
    MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'
    
    # Mock Simulation Settings
    MOCK_VEHICLE_COUNT = int(os.getenv('MOCK_VEHICLE_COUNT', '50'))
    MOCK_NETWORK_BOUNDS = {
        'min_lat': 48.85,
        'max_lat': 48.86,
        'min_lng': 2.35,
        'max_lng': 2.36,
    }