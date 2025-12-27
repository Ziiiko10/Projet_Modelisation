"""
Vehicle-to-Infrastructure priority management
"""
import time
from typing import Dict, List, Any

class V2IPriorityManager:
    """
    Manages priority for emergency and public transport vehicles
    """
    
    def __init__(self):
        self.priority_vehicles = {}
        self.green_wave_routes = {}
    
    def register_priority_vehicle(self, vehicle_data: Dict) -> Dict:
        """
        Register a vehicle for priority treatment
        """
        vehicle_id = vehicle_data['id']
        vehicle_type = vehicle_data['type']
        priority_level = self._get_priority_level(vehicle_type)
        
        self.priority_vehicles[vehicle_id] = {
            **vehicle_data,
            'priority_level': priority_level,
            'registered_at': time.time(),
            'active': True,
            'current_location': vehicle_data.get('position'),
            'destination': vehicle_data.get('destination'),
            'estimated_arrival': None
        }
        
        return {
            'vehicle_id': vehicle_id,
            'priority_level': priority_level,
            'message': f'Vehicle registered with {priority_level} priority',
            'benefits': self._get_priority_benefits(priority_level)
        }
    
    def create_green_wave(self, route: List[Dict], vehicle_type: str = 'emergency') -> Dict:
        """
        Create a green wave for priority vehicle
        """
        route_id = f"green_wave_{int(time.time())}"
        
        # Calculate optimal timings
        intersections = []
        total_time = 0
        
        for i, segment in enumerate(route):
            intersection_id = segment.get('intersection_id')
            distance = segment.get('distance_km', 1)
            
            # Calculate arrival time at intersection
            speed = 60 if vehicle_type == 'emergency' else 40  # km/h
            travel_time = (distance / speed) * 60  # minutes
            
            total_time += travel_time
            
            intersections.append({
                'intersection_id': intersection_id,
                'estimated_arrival': total_time,
                'green_window_start': max(0, total_time - 0.5),  # 30 seconds before
                'green_window_end': total_time + 0.5,  # 30 seconds after
                'priority': 'high' if vehicle_type == 'emergency' else 'medium'
            })
        
        self.green_wave_routes[route_id] = {
            'intersections': intersections,
            'total_duration_min': total_time,
            'vehicle_type': vehicle_type,
            'created_at': time.time(),
            'active': True
        }
        
        return {
            'route_id': route_id,
            'intersections': len(intersections),
            'total_duration_min': round(total_time, 2),
            'green_wave_created': True
        }
    
    def get_intersection_priority(self, intersection_id: str) -> List[Dict]:
        """
        Get priority requests for an intersection
        """
        priorities = []
        current_time = time.time()
        
        # Check for priority vehicles approaching
        for vehicle_id, vehicle_data in self.priority_vehicles.items():
            if vehicle_data['active']:
                # Mock: Check if vehicle is approaching this intersection
                if self._is_approaching(vehicle_data, intersection_id):
                    priorities.append({
                        'vehicle_id': vehicle_id,
                        'vehicle_type': vehicle_data['type'],
                        'priority_level': vehicle_data['priority_level'],
                        'estimated_arrival_sec': 30,  # Mock value
                        'requested_action': 'extend_green',
                        'extension_seconds': self._get_green_extension(vehicle_data['priority_level'])
                    })
        
        # Check for active green waves
        for route_id, route_data in self.green_wave_routes.items():
            if route_data['active']:
                for intersection in route_data['intersections']:
                    if intersection['intersection_id'] == intersection_id:
                        priorities.append({
                            'route_id': route_id,
                            'vehicle_type': route_data['vehicle_type'],
                            'priority_level': 'high' if route_data['vehicle_type'] == 'emergency' else 'medium',
                            'estimated_arrival_sec': intersection['estimated_arrival'] * 60,
                            'requested_action': 'schedule_green',
                            'green_window': {
                                'start': intersection['green_window_start'],
                                'end': intersection['green_window_end']
                            }
                        })
        
        return priorities
    
    def _get_priority_level(self, vehicle_type: str) -> str:
        """Determine priority level based on vehicle type"""
        priority_map = {
            'emergency': 'highest',
            'fire_truck': 'highest',
            'ambulance': 'highest',
            'police': 'highest',
            'bus': 'high',
            'tram': 'high',
            'truck': 'medium',
            'passenger': 'normal',
            'motorcycle': 'normal',
            'bicycle': 'low'
        }
        return priority_map.get(vehicle_type, 'normal')
    
    def _get_priority_benefits(self, priority_level: str) -> List[str]:
        """Get benefits for each priority level"""
        benefits = {
            'highest': ['Green wave', 'Right of way', 'Red light override', 'Cleared intersections'],
            'high': ['Extended green time', 'Priority lanes', 'Reduced waiting'],
            'medium': ['Optimized routing', 'Traffic information'],
            'normal': ['Standard routing'],
            'low': ['Safety warnings']
        }
        return benefits.get(priority_level, [])
    
    def _is_approaching(self, vehicle_data: Dict, intersection_id: str) -> bool:
        """Check if vehicle is approaching intersection (mock)"""
        # In real implementation, use location and route data
        return True  # Mock
    
    def _get_green_extension(self, priority_level: str) -> int:
        """Get green light extension time based on priority"""
        extensions = {
            'highest': 30,
            'high': 15,
            'medium': 10,
            'normal': 0,
            'low': 0
        }
        return extensions.get(priority_level, 0)