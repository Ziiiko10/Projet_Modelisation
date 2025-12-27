"""
Vehicle management for simulation
"""
import random
import time
from typing import Dict, List, Any
from datetime import datetime

class VehicleManager:
    """
    Manages vehicles in the simulation
    """
    
    def __init__(self):
        self.vehicles = {}
        self.vehicle_history = []
        self.next_vehicle_id = 1
    
    def create_vehicle(self, vehicle_type: str = 'passenger', **kwargs) -> Dict:
        """Create a new vehicle"""
        vehicle_id = f"veh_{self.next_vehicle_id:04d}"
        self.next_vehicle_id += 1
        
        # Default vehicle properties
        vehicle = {
            'id': vehicle_id,
            'type': vehicle_type,
            'position': kwargs.get('position', {'lat': 48.8566, 'lng': 2.3522}),
            'speed': kwargs.get('speed', random.uniform(30.0, 60.0)),
            'lane': kwargs.get('lane', 'edge_1_lane_0'),
            'route': kwargs.get('route', ['edge_1', 'edge_2', 'edge_3']),
            'color': self._get_color_for_type(vehicle_type),
            'heading': kwargs.get('heading', random.uniform(0, 360)),
            'created_at': time.time(),
            'updated_at': time.time(),
            'distance_traveled': 0,
            'status': 'active'
        }
        
        # Add specific properties based on type
        if vehicle_type == 'emergency':
            vehicle.update({
                'siren_active': True,
                'priority_level': 'highest',
                'destination': kwargs.get('destination', 'Hospital')
            })
        elif vehicle_type == 'bus':
            vehicle.update({
                'passenger_count': random.randint(0, 50),
                'route_number': random.randint(1, 100)
            })
        elif vehicle_type == 'truck':
            vehicle.update({
                'cargo_type': random.choice(['general', 'hazardous', 'refrigerated', 'bulk']),
                'weight_tons': random.uniform(5.0, 40.0)
            })
        
        self.vehicles[vehicle_id] = vehicle
        self._record_history(vehicle)
        
        return vehicle
    
    def update_vehicle(self, vehicle_id: str, updates: Dict) -> bool:
        """Update vehicle properties"""
        if vehicle_id not in self.vehicles:
            return False
        
        vehicle = self.vehicles[vehicle_id]
        
        # Update allowed fields
        allowed_fields = ['position', 'speed', 'lane', 'route', 'heading', 'status']
        for field in allowed_fields:
            if field in updates:
                vehicle[field] = updates[field]
        
        vehicle['updated_at'] = time.time()
        
        # Calculate distance traveled if position changed
        if 'position' in updates:
            # Simple distance calculation (in reality, use proper geodetic distance)
            old_pos = self._get_last_position(vehicle_id)
            if old_pos:
                dist = abs(updates['position']['lat'] - old_pos['lat']) + abs(updates['position']['lng'] - old_pos['lng'])
                vehicle['distance_traveled'] += dist * 111  # Approximate km (1 degree ≈ 111km)
        
        self._record_history(vehicle)
        return True
    
    def remove_vehicle(self, vehicle_id: str) -> bool:
        """Remove vehicle from simulation"""
        if vehicle_id in self.vehicles:
            vehicle = self.vehicles[vehicle_id]
            vehicle['status'] = 'removed'
            vehicle['removed_at'] = time.time()
            self._record_history(vehicle)
            del self.vehicles[vehicle_id]
            return True
        return False
    
    def get_vehicle(self, vehicle_id: str) -> Dict:
        """Get vehicle by ID"""
        return self.vehicles.get(vehicle_id)
    
    def get_all_vehicles(self, filter_status: str = None) -> List[Dict]:
        """Get all vehicles, optionally filtered by status"""
        if filter_status:
            return [v for v in self.vehicles.values() if v.get('status') == filter_status]
        return list(self.vehicles.values())
    
    def get_vehicles_by_type(self, vehicle_type: str) -> List[Dict]:
        """Get vehicles by type"""
        return [v for v in self.vehicles.values() if v.get('type') == vehicle_type]
    
    def get_vehicle_history(self, vehicle_id: str, limit: int = 100) -> List[Dict]:
        """Get history for a specific vehicle"""
        history = [h for h in self.vehicle_history if h.get('vehicle_id') == vehicle_id]
        return history[-limit:] if history else []
    
    def get_vehicle_statistics(self) -> Dict:
        """Get statistics about all vehicles"""
        total_vehicles = len(self.vehicles)
        
        if total_vehicles == 0:
            return {
                'total': 0,
                'by_type': {},
                'avg_speed': 0,
                'total_distance': 0
            }
        
        # Count by type
        type_counts = {}
        total_speed = 0
        total_distance = 0
        
        for vehicle in self.vehicles.values():
            v_type = vehicle.get('type', 'unknown')
            type_counts[v_type] = type_counts.get(v_type, 0) + 1
            total_speed += vehicle.get('speed', 0)
            total_distance += vehicle.get('distance_traveled', 0)
        
        return {
            'total': total_vehicles,
            'by_type': type_counts,
            'avg_speed': round(total_speed / total_vehicles, 1),
            'total_distance': round(total_distance, 2),
            'active_vehicles': len([v for v in self.vehicles.values() if v.get('status') == 'active']),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def simulate_movement(self, delta_time: float = 1.0):
        """Simulate vehicle movement for a time step"""
        for vehicle_id, vehicle in self.vehicles.items():
            if vehicle.get('status') != 'active':
                continue
            
            # Update position based on speed and heading
            speed_mps = vehicle['speed'] / 3.6  # Convert km/h to m/s
            distance = speed_mps * delta_time
            
            # Convert distance to degrees (approximate)
            lat_distance = distance / 111000  # 1 degree latitude ≈ 111km
            lng_distance = distance / (111000 * 0.707)  # Adjust for longitude at ~45° latitude
            
            # Calculate new position based on heading
            heading_rad = vehicle['heading'] * 3.14159 / 180
            
            new_lat = vehicle['position']['lat'] + lat_distance * (3.14159 / 2 - heading_rad if heading_rad != 0 else 0)
            new_lng = vehicle['position']['lng'] + lng_distance * heading_rad
            
            # Keep within reasonable bounds
            new_lat = max(48.85, min(48.86, new_lat))
            new_lng = max(2.35, min(2.36, new_lng))
            
            # Update vehicle
            self.update_vehicle(vehicle_id, {
                'position': {'lat': new_lat, 'lng': new_lng},
                'speed': vehicle