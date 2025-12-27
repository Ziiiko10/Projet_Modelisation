"""
Vehicle validation schemas
"""

def validate_vehicle_position(data):
    """Validate vehicle position data"""
    if 'position' not in data:
        return False, 'Missing position field'
    
    position = data['position']
    
    if 'lat' not in position or 'lng' not in position:
        return False, 'Position must have lat and lng fields'
    
    # Validate latitude range (-90 to 90)
    if not -90 <= position['lat'] <= 90:
        return False, 'Latitude must be between -90 and 90'
    
    # Validate longitude range (-180 to 180)
    if not -180 <= position['lng'] <= 180:
        return False, 'Longitude must be between -180 and 180'
    
    return True, ''

def validate_vehicle_type(vehicle_type):
    """Validate vehicle type"""
    valid_types = ['passenger', 'emergency', 'bus', 'truck', 'motorcycle', 'bicycle']
    
    if vehicle_type not in valid_types:
        return False, f'Invalid vehicle type. Must be one of: {", ".join(valid_types)}'
    
    return True, ''

def validate_vehicle_data(data, for_update=False):
    """Validate complete vehicle data"""
    if not for_update:
        # For creation, type is required
        if 'type' not in data:
            return False, 'Vehicle type is required'
        
        if not validate_vehicle_type(data['type'])[0]:
            return validate_vehicle_type(data['type'])
    
    # Validate position if provided
    if 'position' in data:
        valid, msg = validate_vehicle_position({'position': data['position']})
        if not valid:
            return False, msg
    
    # Validate speed if provided
    if 'speed' in data and (not isinstance(data['speed'], (int, float)) or data['speed'] < 0 or data['speed'] > 200):
        return False, 'Speed must be a number between 0 and 200 km/h'
    
    return True, ''