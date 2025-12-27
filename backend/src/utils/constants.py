"""
Constants for traffic simulation
"""

class TrafficConstants:
    """Traffic simulation constants"""
    
    # Simulation constants
    SIMULATION_UPDATE_INTERVAL = 0.1  # seconds
    MAX_SIMULATION_SPEED = 10.0
    MIN_SIMULATION_SPEED = 0.1
    
    # Vehicle constants
    VEHICLE_TYPES = ['passenger', 'emergency', 'bus', 'truck', 'motorcycle', 'bicycle']
    VEHICLE_COLORS = {
        'passenger': '#3b82f6',  # blue
        'emergency': '#ef4444',  # red
        'bus': '#f59e0b',        # orange
        'truck': '#8b5cf6',      # purple
        'motorcycle': '#10b981', # green
        'bicycle': '#06b6d4'     # cyan
    }
    
    VEHICLE_SPEED_RANGES = {
        'passenger': (30, 60),    # km/h
        'emergency': (60, 90),    # km/h
        'bus': (20, 40),         # km/h
        'truck': (30, 70),       # km/h
        'motorcycle': (40, 80),  # km/h
        'bicycle': (15, 25)      # km/h
    }
    
    # Traffic light constants
    TRAFFIC_LIGHT_STATES = {
        'G': 'green',
        'y': 'yellow',
        'r': 'red'
    }
    
    DEFAULT_PHASES = [
        {'duration': 30, 'state': 'GGGrrr'},
        {'duration': 5, 'state': 'yyyrrr'},
        {'duration': 30, 'state': 'rrrGGG'},
        {'duration': 5, 'state': 'rrryyy'}
    ]
    
    # Traffic density levels
    TRAFFIC_DENSITY = {
        'very-low': {'vehicles_per_km2': 50, 'avg_speed': 55},
        'low': {'vehicles_per_km2': 100, 'avg_speed': 50},
        'medium': {'vehicles_per_km2': 200, 'avg_speed': 40},
        'high': {'vehicles_per_km2': 300, 'avg_speed': 30},
        'very-high': {'vehicles_per_km2': 400, 'avg_speed': 20}
    }
    
    # Congestion levels
    CONGESTION_THRESHOLDS = {
        'low': {'speed_threshold': 50, 'color': '#10b981'},      # green
        'medium': {'speed_threshold': 30, 'color': '#f59e0b'},   # orange
        'high': {'speed_threshold': 20, 'color': '#ef4444'}      # red
    }
    
    # CO2 emission factors (g/km)
    CO2_EMISSIONS = {
        'passenger': 120,
        'emergency': 180,
        'bus': 80,
        'truck': 150,
        'motorcycle': 60,
        'bicycle': 0
    }
    
    # Time constants
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_MINUTE = 60
    
    # Distance constants (approximate)
    KM_PER_DEGREE_LAT = 111.0
    KM_PER_DEGREE_LNG = 111.0 * 0.707  # At ~45° latitude
    
    # Network constants
    DEFAULT_NETWORK_BOUNDS = {
        'min_lat': 48.85,
        'max_lat': 48.86,
        'min_lng': 2.35,
        'max_lng': 2.36
    }
    
    # API constants
    MAX_VEHICLES_PER_REQUEST = 1000
    MAX_HISTORY_POINTS = 10000
    
    # WebSocket events
    WS_EVENTS = {
        'SIMULATION_UPDATE': 'simulation_update',
        'VEHICLE_UPDATE': 'vehicle_update',
        'TRAFFIC_LIGHT_UPDATE': 'traffic_light_update',
        'METRICS_UPDATE': 'metrics_update',
        'SIMULATION_STATUS': 'simulation_status',
        'ALERT': 'alert',
        'ERROR': 'error'
    }
    
    # Error codes
    ERROR_CODES = {
        'INVALID_SCENARIO': 1001,
        'SIMULATION_RUNNING': 1002,
        'VEHICLE_NOT_FOUND': 1003,
        'INVALID_COMMAND': 1004,
        'DATABASE_ERROR': 1005
    }


class ScenarioConstants:
    """Scenario constants"""
    
    DEFAULT_SCENARIOS = [
        {
            'id': 'default',
            'name': 'Trafic Normal',
            'description': 'Trafic urbain standard',
            'vehicle_count': 100,
            'traffic_density': 'medium',
            'has_emergency_vehicles': False,
            'duration': 3600
        },
        {
            'id': 'rush_hour',
            'name': 'Heure de Pointe',
            'description': 'Pic de trafic du matin',
            'vehicle_count': 250,
            'traffic_density': 'very-high',
            'has_emergency_vehicles': True,
            'duration': 7200
        },
        {
            'id': 'emergency_test',
            'name': 'Test Urgence',
            'description': 'Scénario avec véhicules prioritaires',
            'vehicle_count': 80,
            'traffic_density': 'low',
            'has_emergency_vehicles': True,
            'duration': 1800
        },
        {
            'id': 'weekend',
            'name': 'Week-end Léger',
            'description': 'Trafic réduit de week-end',
            'vehicle_count': 60,
            'traffic_density': 'low',
            'has_emergency_vehicles': False,
            'duration': 5400
        }
    ]