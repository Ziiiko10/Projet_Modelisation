"""
Helper functions for the application
"""
import time
import json
import math
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from flask import jsonify

def format_timestamp(timestamp=None, format_str="%Y-%m-%dT%H:%M:%SZ") -> str:
    """Format timestamp to string"""
    if timestamp is None:
        timestamp = datetime.utcnow()
    elif isinstance(timestamp, (int, float)):
        timestamp = datetime.fromtimestamp(timestamp)
    
    return timestamp.strftime(format_str)

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse timestamp string to datetime"""
    try:
        # Try ISO format first
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except ValueError:
        # Try other common formats
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")

def calculate_distance(pos1: Dict, pos2: Dict) -> float:
    """
    Calculate distance between two coordinates in kilometers
    Using Haversine formula
    """
    # Earth radius in kilometers
    R = 6371.0
    
    lat1 = math.radians(pos1['lat'])
    lon1 = math.radians(pos1['lng'])
    lat2 = math.radians(pos2['lat'])
    lon2 = math.radians(pos2['lng'])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def validate_coordinates(lat: float, lng: float) -> bool:
    """Validate latitude and longitude coordinates"""
    return -90 <= lat <= 90 and -180 <= lng <= 180

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

def format_speed(speed_kmh: float) -> str:
    """Format speed with unit"""
    return f"{speed_kmh:.1f} km/h"

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def generate_id(prefix: str = "id") -> str:
    """Generate unique ID"""
    timestamp = int(time.time() * 1000)
    random_suffix = format(timestamp % 10000, '04d')
    return f"{prefix}_{timestamp}_{random_suffix}"

def safe_json_loads(data: str, default=None):
    """Safely parse JSON string"""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(data: Any, default=None) -> str:
    """Safely dump to JSON string"""
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError):
        return default or "{}"

def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Create success JSON response"""
    response = {
        'success': True,
        'message': message,
        'timestamp': format_timestamp()
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def error_response(message: str = "Error", error_code: int = None, status_code: int = 400):
    """Create error JSON response"""
    response = {
        'success': False,
        'message': message,
        'timestamp': format_timestamp()
    }
    
    if error_code is not None:
        response['error_code'] = error_code
    
    return jsonify(response), status_code

def calculate_congestion_level(avg_speed: float, total_vehicles: int) -> str:
    """Calculate congestion level based on speed and vehicle count"""
    if avg_speed > 50 and total_vehicles < 100:
        return 'low'
    elif avg_speed > 30:
        return 'medium'
    else:
        return 'high'

def estimate_travel_time(distance_km: float, avg_speed_kmh: float, congestion: str = 'medium') -> float:
    """Estimate travel time considering congestion"""
    # Congestion factors
    congestion_factors = {
        'low': 1.0,
        'medium': 1.3,
        'high': 1.7,
        'very-high': 2.2
    }
    
    factor = congestion_factors.get(congestion, 1.3)
    effective_speed = avg_speed_kmh / factor
    
    if effective_speed <= 0:
        return float('inf')
    
    return (distance_km / effective_speed) * 60  # in minutes

def filter_none_values(data: Dict) -> Dict:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries, dict2 overwrites dict1"""
    result = dict1.copy()
    result.update(dict2)
    return result

def format_large_number(number: float) -> str:
    """Format large numbers with K, M suffixes"""
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return f"{number:.0f}"

def get_time_of_day(hour: int = None) -> str:
    """Get time of day category"""
    if hour is None:
        hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 22:
        return 'evening'
    else:
        return 'night'