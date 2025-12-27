import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de l'application Flask"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'urbanflow-dev-secret-2024')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # WebSocket
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = CORS_ORIGINS
    SOCKETIO_PING_TIMEOUT = 60
    SOCKETIO_PING_INTERVAL = 25
    
    # Simulation
    SIMULATION_UPDATE_INTERVAL = float(os.getenv('SIMULATION_UPDATE_INTERVAL', '0.1'))  # 100ms
    MOCK_MODE = os.getenv('MOCK_MODE', 'true').lower() == 'true'
    
    # Mock Simulation
    MOCK_VEHICLE_COUNT = int(os.getenv('MOCK_VEHICLE_COUNT', '50'))
    MOCK_TRAFFIC_LIGHT_COUNT = int(os.getenv('MOCK_TRAFFIC_LIGHT_COUNT', '4'))
    MOCK_SIMULATION_SPEED = float(os.getenv('MOCK_SIMULATION_SPEED', '1.0'))
    
    # Network bounds for mock data (Paris area)
    MOCK_NETWORK_BOUNDS = {
        'min_lat': 48.85,
        'max_lat': 48.86,
        'min_lng': 2.35,
        'max_lng': 2.36,
        'center_lat': 48.8566,
        'center_lng': 2.3522
    }
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')