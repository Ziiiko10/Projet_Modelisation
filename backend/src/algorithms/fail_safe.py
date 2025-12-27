"""
Fall-safe traffic management algorithm
"""
import time
from typing import Dict, Any

class FailSafeAlgorithm:
    """Fallback algorithm for traffic management"""
    
    def __init__(self):
        self.name = "Fail-Safe Algorithm"
        self.description = "Basic fallback algorithm for traffic management"
        self.last_update = time.time()
    
    def calculate_phases(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate traffic light phases based on simple rules
        """
        phases = []
        
        # Simple alternating phases
        phases.append({
            'id': 'phase_1',
            'duration': 30,
            'state': 'GGGrrr',
            'description': 'Main road green'
        })
        
        phases.append({
            'id': 'phase_2',
            'duration': 5,
            'state': 'yyyrrr',
            'description': 'Main road yellow'
        })
        
        phases.append({
            'id': 'phase_3',
            'duration': 30,
            'state': 'rrrGGG',
            'description': 'Side road green'
        })
        
        phases.append({
            'id': 'phase_4',
            'duration': 5,
            'state': 'rrryyy',
            'description': 'Side road yellow'
        })
        
        return {
            'algorithm': self.name,
            'phases': phases,
            'cycle_time': 70,
            'timestamp': time.time()
        }
    
    def optimize_intersection(self, intersection_id: str, traffic_data: Dict) -> Dict:
        """
        Optimize a specific intersection
        """
        vehicle_count = traffic_data.get('vehicle_count', 0)
        emergency_vehicles = traffic_data.get('emergency_vehicles', 0)
        
        # Adjust phase durations based on traffic
        base_green = 30
        if vehicle_count > 10:
            base_green = 40
        if emergency_vehicles > 0:
            base_green = 45  # Give more time for emergency vehicles
        
        return {
            'intersection_id': intersection_id,
            'action': 'adjust_phases',
            'parameters': {
                'main_green': base_green,
                'side_green': base_green - 10,
                'yellow_time': 5,
                'all_red': 2
            },
            'reason': f'Traffic: {vehicle_count} vehicles, Emergencies: {emergency_vehicles}'
        }