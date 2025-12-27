"""
Mock data generation utilities
"""
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class MockDataGenerator:
    """
    Generates mock data for development and testing
    """
    
    @staticmethod
    def generate_scenario(scenario_id: str = None) -> Dict:
        """Generate a mock scenario"""
        scenarios = [
            {
                'id': 'morning_rush',
                'name': 'Heure de pointe du matin',
                'description': 'Trafic dense de 7h à 9h',
                'vehicle_count': 200,
                'traffic_density': 'very-high',
                'has_emergency_vehicles': True,
                'duration': 7200,
                'time_of_day': 'morning'
            },
            {
                'id': 'evening_commute',
                'name': 'Retour du travail',
                'description': 'Pic de trafic de 17h à 19h',
                'vehicle_count': 180,
                'traffic_density': 'high',
                'has_emergency_vehicles': False,
                'duration': 7200,
                'time_of_day': 'evening'
            },
            {
                'id': 'weekend_leisure',
                'name': 'Trafic de week-end',
                'description': 'Trafic léger avec plus de piétons et vélos',
                'vehicle_count': 80,
                'traffic_density': 'low',
                'has_emergency_vehicles': False,
                'duration': 10800,
                'time_of_day': 'afternoon'
            },
            {
                'id': 'event_traffic',
                'name': 'Événement spécial',
                'description': 'Afflux de véhicules vers un événement',
                'vehicle_count': 150,
                'traffic_density': 'high',
                'has_emergency_vehicles': True,
                'duration': 5400,
                'time_of_day': 'evening'
            }
        ]
        
        if scenario_id:
            for scenario in scenarios:
                if scenario['id'] == scenario_id:
                    return scenario
            return scenarios[0]
        
        return random.choice(scenarios)
    
    @staticmethod
    def generate_vehicles(count: int = 50) -> List[Dict]:
        """Generate mock vehicles"""
        vehicles = []
        vehicle_types = ['passenger', 'bus', 'truck', 'motorcycle', 'bicycle', 'emergency']
        colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4']
        
        for i in range(count):
            vehicle_type = random.choice(vehicle_types)
            color = colors[vehicle_types.index(vehicle_type) % len(colors)]
            
            vehicle = {
                'id': f'veh_{i:04d}',
                'type': vehicle_type,
                'position': {
                    'lat': round(48.8566 + random.uniform(-0.005, 0.005), 6),
                    'lng': round(2.3522 + random.uniform(-0.005, 0.005), 6)
                },
                'speed': round(random.uniform(20.0, 70.0), 1),
                'lane': f'edge_{random.randint(1, 5)}_lane_{random.randint(0, 1)}',
                'route': [f'edge_{j}' for j in random.sample(range(1, 6), 3)],
                'color': color,
                'heading': random.uniform(0, 360),
                'created_at': datetime.utcnow().isoformat()
            }
            
            if vehicle_type == 'emergency':
                vehicle['siren_active'] = random.choice([True, False])
                vehicle['priority'] = 'highest'
            
            vehicles.append(vehicle)
        
        return vehicles
    
    @staticmethod
    def generate_traffic_lights(count: int = 5) -> List[Dict]:
        """Generate mock traffic lights"""
        traffic_lights = []
        positions = [
            {'lat': 48.8566, 'lng': 2.3522},
            {'lat': 48.8560, 'lng': 2.3530},
            {'lat': 48.8555, 'lng': 2.3515},
            {'lat': 48.8570, 'lng': 2.3528},
            {'lat': 48.8562, 'lng': 2.3510}
        ]
        
        phase_patterns = [
            [
                {'duration': 30, 'state': 'GGGrrr'},
                {'duration': 5, 'state': 'yyyrrr'},
                {'duration': 30, 'state': 'rrrGGG'},
                {'duration': 5, 'state': 'rrryyy'}
            ],
            [
                {'duration': 25, 'state': 'GGrrGG'},
                {'duration': 5, 'state': 'yyrryy'},
                {'duration': 25, 'state': 'rrGGrr'},
                {'duration': 5, 'state': 'rryyrr'}
            ],
            [
                {'duration': 40, 'state': 'GGGrrr'},
                {'duration': 5, 'state': 'yyyrrr'},
                {'duration': 20, 'state': 'rrrGGG'},
                {'duration': 5, 'state': 'rrryyy'}
            ]
        ]
        
        for i in range(min(count, len(positions))):
            phases = random.choice(phase_patterns)
            
            traffic_light = {
                'id': f'tl_{i+1:03d}',
                'position': positions[i],
                'state': phases[0]['state'],
                'currentPhase': 0,
                'phases': phases,
                'lastChange': datetime.utcnow().isoformat(),
                'efficiency': round(random.uniform(0.7, 0.95), 2)
            }
            
            traffic_lights.append(traffic_light)
        
        return traffic_lights
    
    @staticmethod
    def generate_metrics(time_range: str = 'current') -> Dict:
        """Generate mock metrics"""
        base_metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'totalVehicles': random.randint(50, 200),
            'avgSpeed': round(random.uniform(30.0, 60.0), 1),
            'avgTravelTime': round(random.uniform(40.0, 90.0), 1),
            'co2Emissions': round(random.uniform(100.0, 300.0), 1),
            'queueLengths': {
                'intersection_1': random.randint(0, 10),
                'intersection_2': random.randint(0, 15),
                'intersection_3': random.randint(0, 8),
                'intersection_4': random.randint(0, 12)
            },
            'emergencyVehiclesActive': random.randint(0, 3),
            'throughput': random.randint(500, 1500),
            'congestionLevel': random.choice(['low', 'medium', 'high']),
            'accidentsReported': random.randint(0, 2)
        }
        
        if time_range == 'hourly':
            # Generate hourly data for the past 24 hours
            metrics_list = []
            current_time = datetime.utcnow()
            
            for i in range(24):
                hour_time = current_time - timedelta(hours=i)
                hour_metrics = base_metrics.copy()
                hour_metrics['timestamp'] = hour_time.isoformat()
                hour_metrics['totalVehicles'] = random.randint(20, 100) if i > 18 or i < 6 else random.randint(100, 250)
                hour_metrics['avgSpeed'] = round(random.uniform(40.0, 70.0) if i > 18 or i < 6 else random.uniform(20.0, 50.0), 1)
                metrics_list.append(hour_metrics)
            
            return {'hourly': metrics_list[::-1]}  # Reverse to have chronological order
        
        return base_metrics
    
    @staticmethod
    def generate_network_data() -> Dict:
        """Generate mock network data"""
        nodes = []
        edges = []
        
        # Generate nodes (intersections)
        for i in range(10):
            node = {
                'id': f'node_{i}',
                'position': {
                    'lat': 48.8560 + (i % 5) * 0.0005,
                    'lng': 2.3520 + (i // 5) * 0.0005
                },
                'type': 'intersection',
                'traffic_light': i < 5  # First 5 have traffic lights
            }
            nodes.append(node)
        
        # Generate edges (roads)
        edge_id = 0
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if random.random() > 0.7:  # 30% chance of connection
                    edge = {
                        'id': f'edge_{edge_id}',
                        'from': nodes[i]['id'],
                        'to': nodes[j]['id'],
                        'length': round(random.uniform(0.5, 2.0), 2),  # km
                        'lanes': random.randint(1, 3),
                        'speed_limit': random.choice([30, 50, 70]),
                        'type': random.choice(['highway', 'avenue', 'street'])
                    }
                    edges.append(edge)
                    edge_id += 1
        
        return {
            'nodes': nodes,
            'edges': edges,
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def generate_alerts(count: int = 3) -> List[Dict]:
        """Generate mock alerts"""
        alert_types = ['accident', 'congestion', 'road_work', 'weather', 'special_event']
        severities = ['low', 'medium', 'high', 'critical']
        
        alerts = []
        for i in range(count):
            alert = {
                'id': f'alert_{i+1:03d}',
                'type': random.choice(alert_types),
                'severity': random.choice(severities),
                'message': f'Alerte {i+1}: {random.choice(alert_types).replace("_", " ").title()}',
                'position': {
                    'lat': round(48.8566 + random.uniform(-0.01, 0.01), 6),
                    'lng': round(2.3522 + random.uniform(-0.01, 0.01), 6)
                },
                'radius': random.uniform(0.1, 1.0),  # km
                'start_time': datetime.utcnow().isoformat(),
                'expected_duration': random.randint(30, 180),  # minutes
                'affected_routes': [f'edge_{j}' for j in random.sample(range(1, 6), random.randint(1, 3))],
                'status': 'active'
            }
            alerts.append(alert)
        
        return alerts