"""
WebSocket event definitions
"""

class WebSocketEvents:
    """WebSocket event constants and helpers"""
    
    # Client → Server events
    CLIENT_EVENTS = {
        'CONNECT': 'connect',
        'DISCONNECT': 'disconnect',
        'COMMAND': 'command',
        'EMERGENCY_VEHICLE': 'emergency_vehicle',
        'CHANGE_SCENARIO': 'change_scenario',
        'SUBSCRIBE': 'subscribe',
        'UNSUBSCRIBE': 'unsubscribe',
        'GET_STATUS': 'get_status',
        'PING': 'ping'
    }
    
    # Server → Client events
    SERVER_EVENTS = {
        'SIMULATION_UPDATE': 'simulation_update',
        'VEHICLE_UPDATE': 'vehicle_update',
        'TRAFFIC_LIGHT_UPDATE': 'traffic_light_update',
        'METRICS_UPDATE': 'metrics_update',
        'SIMULATION_STATUS': 'simulation_status',
        'NOTIFICATION': 'notification',
        'EMERGENCY_ALERT': 'emergency_alert',
        'ALERT': 'alert',
        'ERROR': 'error',
        'SUBSCRIPTION_UPDATE': 'subscription_update',
        'PONG': 'pong'
    }
    
    # Event data schemas
    @staticmethod
    def create_simulation_update(data: dict) -> dict:
        """Create simulation update event data"""
        return {
            'type': 'simulation_update',
            'data': data,
            'timestamp': '2024-01-25T14:30:00Z'
        }
    
    @staticmethod
    def create_vehicle_update(vehicles: list) -> dict:
        """Create vehicle update event data"""
        return {
            'type': 'vehicle_update',
            'vehicles': vehicles,
            'count': len(vehicles),
            'timestamp': '2024-01-25T14:30:00Z'
        }
    
    @staticmethod
    def create_traffic_light_update(traffic_lights: list) -> dict:
        """Create traffic light update event data"""
        return {
            'type': 'traffic_light_update',
            'traffic_lights': traffic_lights,
            'timestamp': '2024-01-25T14:30:00Z'
        }
    
    @staticmethod
    def create_metrics_update(metrics: dict) -> dict:
        """Create metrics update event data"""
        return {
            'type': 'metrics_update',
            'metrics': metrics,
            'timestamp': '2024-01-25T14:30:00Z'
        }
    
    @staticmethod
    def create_simulation_status(status: str, details: dict = None) -> dict:
        """Create simulation status event data"""
        data = {
            'type': 'simulation_status',
            'status': status,
            'timestamp': '2024-01-25T14:30:00Z'
        }
        
        if details:
            data.update(details)
        
        return data
    
    @staticmethod
    def create_notification(message: str, notification_type: str = 'info', data: dict = None) -> dict:
        """Create notification event data"""
        notification = {
            'type': 'notification',
            'notification_type': notification_type,
            'message': message,
            'timestamp': '2024-01-25T14:30:00Z'
        }
        
        if data:
            notification['data'] = data
        
        return notification
    
    @staticmethod
    def create_emergency_alert(message: str, vehicle: dict = None) -> dict:
        """Create emergency alert event data"""
        alert = {
            'type': 'emergency_alert',
            'message': message,
            'priority': 'high',
            'timestamp': '2024-01-25T14:30:00Z'
        }
        
        if vehicle:
            alert['vehicle'] = vehicle
        
        return alert
    
    @staticmethod
    def create_error(message: str, error_code: str = None) -> dict:
        """Create error event data"""
        error = {
            'type': 'error',
            'message': message,
            'timestamp': '2024-01-25T14:30:00Z'
        }
        
        if error_code:
            error['error_code'] = error_code
        
        return error
    
    @staticmethod
    def validate_event_data(event_type: str, data: dict) -> bool:
        """Validate event data structure"""
        validators = {
            'command': lambda d: 'command' in d,
            'emergency_vehicle': lambda d: True,  # No required fields
            'change_scenario': lambda d: 'scenario_id' in d,
            'subscribe': lambda d: 'event_type' in d,
            'unsubscribe': lambda d: 'event_type' in d
        }
        
        validator = validators.get(event_type)
        if validator:
            return validator(data)
        
        return True  # Unknown event types are accepted