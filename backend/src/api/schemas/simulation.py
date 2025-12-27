"""
Simulation validation schemas
"""

def validate_scenario(data):
    """Validate scenario data"""
    required_fields = ['id', 'name']
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
    
    # Validate traffic density
    if 'trafficDensity' in data and data['trafficDensity'] not in ['low', 'medium', 'high', 'very-high']:
        return False, 'Invalid traffic density value'
    
    # Validate vehicle count
    if 'vehicleCount' in data and not isinstance(data['vehicleCount'], int):
        return False, 'Vehicle count must be integer'
    
    # Validate duration
    if 'duration' in data and not isinstance(data['duration'], int):
        return False, 'Duration must be integer'
    
    return True, ''

def validate_simulation_command(data):
    """Validate simulation command"""
    valid_commands = ['start', 'pause', 'resume', 'stop', 'reset', 'speed']
    
    if 'command' not in data:
        return False, 'Missing command field'
    
    if data['command'] not in valid_commands:
        return False, f'Invalid command. Must be one of: {", ".join(valid_commands)}'
    
    if data['command'] == 'start' and 'scenario_id' not in data:
        return False, 'Missing scenario_id for start command'
    
    if data['command'] == 'speed' and 'speed' not in data:
        return False, 'Missing speed value for speed command'
    
    return True, ''