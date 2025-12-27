"""
Traffic optimization algorithms
"""
import time
import random
from typing import Dict, List, Any

class TrafficOptimizer:
    """
    Various traffic optimization techniques
    """
    
    def __init__(self):
        self.optimization_history = []
    
    def optimize_route(self, vehicle_data: Dict, network_data: Dict) -> Dict:
        """
        Optimize route for a vehicle
        """
        start = vehicle_data.get('start')
        end = vehicle_data.get('end')
        vehicle_type = vehicle_data.get('type', 'passenger')
        
        # Simple A* like algorithm (simplified for mock)
        routes = self._find_routes(start, end, network_data)
        
        if not routes:
            return {'route': [], 'distance': 0, 'time': 0}
        
        # Select best route based on vehicle type
        if vehicle_type == 'emergency':
            # Emergency vehicles prefer shortest time
            best_route = min(routes, key=lambda r: r['estimated_time'])
        elif vehicle_type == 'truck':
            # Trucks avoid small streets
            best_route = min([r for r in routes if not r.get('has_small_streets', False)], 
                            key=lambda r: r['distance'], 
                            default=routes[0])
        else:
            # Regular vehicles use balanced approach
            best_route = min(routes, key=lambda r: r['distance'] * 0.7 + r['estimated_time'] * 0.3)
        
        return {
            'vehicle_id': vehicle_data.get('id'),
            'vehicle_type': vehicle_type,
            'optimized_route': best_route['path'],
            'distance_km': best_route['distance'],
            'estimated_time_min': best_route['estimated_time'],
            'optimization_type': 'route_optimization'
        }
    
    def optimize_traffic_lights(self, traffic_data: Dict) -> List[Dict]:
        """
        Optimize traffic light timings across network
        """
        intersections = traffic_data.get('intersections', [])
        optimized = []
        
        for intersection in intersections:
            vehicle_count = sum(lane.get('vehicle_count', 0) for lane in intersection.get('lanes', []))
            
            # Adaptive timing based on traffic
            base_green = 30
            if vehicle_count > 20:
                green_time = 45
            elif vehicle_count < 5:
                green_time = 25
            else:
                green_time = base_green
            
            # Emergency vehicle detection
            emergency_count = sum(1 for lane in intersection.get('lanes', []) 
                                if lane.get('has_emergency', False))
            
            if emergency_count > 0:
                # Give priority to emergency vehicles
                green_time = min(60, green_time + 15)
            
            optimization = {
                'intersection_id': intersection['id'],
                'current_green': intersection.get('current_green', base_green),
                'optimized_green': green_time,
                'vehicle_count': vehicle_count,
                'emergency_vehicles': emergency_count,
                'adjustment_percent': ((green_time - base_green) / base_green) * 100,
                'timestamp': time.time()
            }
            
            optimized.append(optimization)
        
        return optimized
    
    def _find_routes(self, start: str, end: str, network: Dict) -> List[Dict]:
        """
        Find possible routes between two points (mock implementation)
        """
        # Mock route finding
        routes = []
        
        # Route 1: Direct route
        routes.append({
            'path': ['edge_1', 'edge_2', 'edge_3'],
            'distance': 2.5,
            'estimated_time': 5,
            'traffic_level': 'medium'
        })
        
        # Route 2: Alternative route
        routes.append({
            'path': ['edge_1', 'edge_5', 'edge_4'],
            'distance': 3.0,
            'estimated_time': 4,
            'traffic_level': 'low',
            'has_small_streets': False
        })
        
        # Route 3: Scenic route
        routes.append({
            'path': ['edge_1', 'edge_2', 'edge_5', 'edge_4'],
            'distance': 4.0,
            'estimated_time': 7,
            'traffic_level': 'low',
            'has_small_streets': True
        })
        
        return routes
    
    def calculate_network_efficiency(self, network_data: Dict) -> Dict:
        """
        Calculate overall network efficiency
        """
        total_vehicles = network_data.get('total_vehicles', 0)
        avg_speed = network_data.get('avg_speed', 30)
        congestion_points = network_data.get('congestion_points', 0)
        
        # Efficiency score (0-100)
        speed_score = min(100, (avg_speed / 60) * 100)  # Max 60 km/h = 100%
        congestion_score = max(0, 100 - (congestion_points * 10))
        flow_score = 100 if total_vehicles > 0 else 0
        
        efficiency_score = (speed_score * 0.4 + congestion_score * 0.4 + flow_score * 0.2)
        
        return {
            'efficiency_score': round(efficiency_score, 2),
            'speed_score': round(speed_score, 2),
            'congestion_score': round(congestion_score, 2),
            'flow_score': round(flow_score, 2),
            'recommendations': self._generate_recommendations(efficiency_score, network_data)
        }
    
    def _generate_recommendations(self, score: float, network_data: Dict) -> List[str]:
        """
        Generate recommendations based on efficiency score
        """
        recommendations = []
        
        if score < 50:
            recommendations.append("Consider implementing traffic restrictions during peak hours")
            recommendations.append("Optimize traffic light synchronization")
            recommendations.append("Add dedicated lanes for public transport")
        
        if score > 80:
            recommendations.append("Traffic flow is efficient - maintain current settings")
        
        congestion = network_data.get('congestion_points', 0)
        if congestion > 5:
            recommendations.append(f"Reduce congestion at {congestion} critical points")
        
        return recommendations