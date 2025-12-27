"""
Data generator for mock simulation
"""
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

class DataGenerator:
    """
    Generates realistic traffic data for mock simulation
    """
    
    def __init__(self, bounds=None):
        self.bounds = bounds or {
            'min_lat': 48.85,
            'max_lat': 48.86,
            'min_lng': 2.35,
            'max_lng': 2.36
        }
        self.road_network = self._generate_road_network()
        self.intersections = self._generate_intersections()
    
    def _generate_road_network(self) -> List[Dict]:
        """Generate a mock road network"""
        network = []
        
        # Create a grid of roads
        lat_step = (self.bounds['max_lat'] - self.bounds['min_lat']) / 4
        lng_step = (self.bounds['max_lng'] - self.bounds['min_lng']) / 4
        
        # Horizontal roads
        for i in range(5):
            lat = self.bounds['min_lat'] + i * lat_step
            network.append({
                'id': f'road_h_{i}',
                'type': 'highway' if i == 2 else 'street',
                'from': {'lat': lat, 'lng': self.bounds['min_lng']},
                'to': {'lat': lat, 'lng': self.bounds['max_lng']},
                'lanes': 2 if i == 2 else 1,
                'speed_limit': 70 if i == 2 else 50,
                'direction': 'bidirectional'
            })
        
        # Vertical roads
        for i in range(5):
            lng = self.bounds['min_lng'] + i * lng_step
            network.append({
                'id': f'road_v_{i}',
                'type': 'avenue' if i == 2 else 'street',
                'from': {'lat': self.bounds['min_lat'], 'lng': lng},
                'to': {'lat': self.bounds['max_lat'], 'lng': lng},
                'lanes': 2 if i == 2 else 1,
                'speed_limit': 60 if i == 2 else 50,
                'direction': 'bidirectional'
            })
        
        return network
    
    def _generate_intersections(self) -> List[Dict]:
        """Generate intersections from road network"""
        intersections = []
        
        # Create intersections at road crossings
        lat_step = (self.bounds['max_lat'] - self.bounds['min_lat']) / 4
        lng_step = (self.bounds['max_lng'] - self.bounds['min_lng']) / 4
        
        for i in range(5):
            for j in range(5):
                lat = self.bounds['min_lat'] + i * lat_step
                lng = self.bounds['min_lng'] + j * lng_step
                
                intersection = {
                    'id': f'intersection_{i}_{j}',
                    'position': {'lat': lat, 'lng': lng},
                    'type': 'signalized' if (i + j) % 2 == 0 else 'unsignalized',
                    'roads': [
                        f'road_h_{i}',
                        f'road_v_{j}'
                    ],
                    'traffic_volume': random.randint(100, 1000),
                    'congestion_index': random.uniform(0, 1)
                }
                
                intersections.append(intersection)
        
        return intersections
    
    def generate_vehicle_data(self, vehicle_type: str = None) -> Dict:
        """Generate realistic vehicle data"""
        if not vehicle_type:
            vehicle_type = random.choice(['passenger', 'bus', 'truck', 'motorcycle', 'bicycle'])
        
        # Vehicle characteristics
        vehicle_specs = {
            'passenger': {
                'length': 4.5,
                'width': 1.8,
                'acceleration': 2.5,
                'deceleration': 4.5,
                'max_speed': 60
            },
            'bus': {
                'length': 12,
                'width': 2.5,
                'acceleration': 1.2,
                'deceleration': 3.0,
                'max_speed': 50
            },
            'truck': {
                'length': 16,
                'width': 2.5,
                'acceleration': 1.0,
                'deceleration': 2.5,
                'max_speed': 70
            },
            'motorcycle': {
                'length': 2.0,
                'width': 0.8,
                'acceleration': 3.5,
                'deceleration': 6.0,
                'max_speed': 80
            },
            'bicycle': {
                'length': 1.8,
                'width': 0.6,
                'acceleration': 1.0,
                'deceleration': 3.0,
                'max_speed': 25
            },
            'emergency': {
                'length': 5.0,
                'width': 2.0,
                'acceleration': 3.0,
                'deceleration': 5.0,
                'max_speed': 90
            }
        }
        
        specs = vehicle_specs.get(vehicle_type, vehicle_specs['passenger'])
        
        # Generate position on a random road
        road = random.choice(self.road_network)
        progress = random.random()
        
        lat = road['from']['lat'] + (road['to']['lat'] - road['from']['lat']) * progress
        lng = road['from']['lng'] + (road['to']['lng'] - road['from']['lng']) * progress
        
        # Determine speed based on road type and vehicle
        max_speed = min(specs['max_speed'], road['speed_limit'])
        speed = random.uniform(max_speed * 0.7, max_speed * 0.9)
        
        return {
            'type': vehicle_type,
            'specifications': specs,
            'position': {'lat': lat, 'lng': lng},
            'speed': round(speed, 1),
            'road_id': road['id'],
            'lane': random.randint(0, road['lanes'] - 1),
            'heading': self._calculate_heading(road, progress),
            'color': self._get_vehicle_color(vehicle_type)
        }
    
    def generate_traffic_metrics(self, time_of_day: str = None) -> Dict:
        """Generate traffic metrics for the network"""
        if not time_of_day:
            hour = datetime.now().hour
            if 7 <= hour < 9 or 17 <= hour < 19:
                time_of_day = 'rush_hour'
            elif 9 <= hour < 17:
                time_of_day = 'daytime'
            else:
                time_of_day = 'night'
        
        # Base metrics by time of day
        base_metrics = {
            'rush_hour': {
                'density': 0.8,
                'avg_speed': 25,
                'congestion_level': 'high',
                'accident_probability': 0.1
            },
            'daytime': {
                'density': 0.5,
                'avg_speed': 40,
                'congestion_level': 'medium',
                'accident_probability': 0.05
            },
            'night': {
                'density': 0.2,
                'avg_speed': 55,
                'congestion_level': 'low',
                'accident_probability': 0.02
            }
        }
        
        metrics = base_metrics.get(time_of_day, base_metrics['daytime'])
        
        # Add some randomness
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'time_of_day': time_of_day,
            'network_density': round(metrics['density'] + random.uniform(-0.1, 0.1), 2),
            'average_speed': round(metrics['avg_speed'] + random.uniform(-5, 5), 1),
            'congestion_level': metrics['congestion_level'],
            'total_vehicles': random.randint(50, 300),
            'active_intersections': len([i for i in self.intersections if i['type'] == 'signalized']),
            'predicted_congestion': self._predict_congestion(time_of_day)
        }
        
        return metrics
    
    def _calculate_heading(self, road: Dict, progress: float) -> float:
        """Calculate vehicle heading based on road direction"""
        dx = road['to']['lng'] - road['from']['lng']
        dy = road['to']['lat'] - road['from']['lat']
        
        # Calculate angle in radians, convert to degrees
        angle = (180 / 3.14159) * (3.14159 / 2 - (0 if dx == 0 else (dy / dx) if dx != 0 else 0))
        
        # Adjust based on direction
        if dx < 0:
            angle += 180
        
        return angle % 360
    
    def _get_vehicle_color(self, vehicle_type: str) -> str:
        """Get color for vehicle type"""
        colors = {
            'passenger': '#3b82f6',  # blue
            'emergency': '#ef4444',  # red
            'bus': '#f59e0b',        # orange
            'truck': '#8b5cf6',      # purple
            'motorcycle': '#10b981', # green
            'bicycle': '#06b6d4'     # cyan
        }
        return colors.get(vehicle_type, '#3b82f6')
    
    def _predict_congestion(self, time_of_day: str) -> List[Dict]:
        """Predict congestion points"""
        predictions = []
        
        # Select random intersections as congestion points
        congestion_intensity = {
            'rush_hour': 0.6,
            'daytime': 0.3,
            'night': 0.1
        }
        
        intensity = congestion_intensity.get(time_of_day, 0.3)
        
        for intersection in random.sample(self.intersections, int(len(self.intersections) * intensity)):
            predictions.append({
                'intersection_id': intersection['id'],
                'position': intersection['position'],
                'severity': random.choice(['low', 'medium', 'high']),
                'expected_duration_min': random.randint(10, 60),
                'cause': random.choice(['accident', 'road_work', 'special_event', 'weather'])
            })
        
        return predictions
    
    def generate_weather_conditions(self) -> Dict:
        """Generate weather conditions affecting traffic"""
        weather_types = ['clear', 'rain', 'snow', 'fog', 'storm']
        weather = random.choice(weather_types)
        
        effects = {
            'clear': {'speed_multiplier': 1.0, 'accident_risk': 0.05, 'visibility': 'excellent'},
            'rain': {'speed_multiplier': 0.8, 'accident_risk': 0.15, 'visibility': 'good'},
            'snow': {'speed_multiplier': 0.5, 'accident_risk': 0.3, 'visibility': 'poor'},
            'fog': {'speed_multiplier': 0.7, 'accident_risk': 0.2, 'visibility': 'very_poor'},
            'storm': {'speed_multiplier': 0.6, 'accident_risk': 0.25, 'visibility': 'poor'}
        }
        
        return {
            'type': weather,
            'effects': effects.get(weather, effects['clear']),
            'temperature': random.uniform(-5, 35),
            'wind_speed': random.uniform(0, 20),
            'timestamp': datetime.utcnow().isoformat()
        }