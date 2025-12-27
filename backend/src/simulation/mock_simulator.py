"""
Mock traffic simulator (replaces SUMO)
"""
import time
import random
import threading
from datetime import datetime
from typing import List, Dict, Any
import json

class MockSimulator:
    """
    Simulates SUMO for frontend development
    Generates realistic vehicle movement data
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.vehicles: List[Dict] = []
        self.traffic_lights: List[Dict] = []
        self.metrics: Dict = {}
        self.is_running = False
        self.is_paused = False
        self.current_scenario = None
        self.simulation_time = 0
        self.start_real_time = None
        self.update_interval = self.config.get('update_interval', 0.1)
        self.network_bounds = self.config.get('network_bounds', {
            'min_lat': 48.85,
            'max_lat': 48.86,
            'min_lng': 2.35,
            'max_lng': 2.36,
        })
        
        # Initialize
        self._initialize_traffic_lights()
        self._initialize_network_edges()
        
        # Statistics
        self.stats = {
            'total_vehicles_created': 0,
            'total_distance_traveled': 0,
            'emergency_vehicles_served': 0
        }
    
    def _initialize_traffic_lights(self):
        """Initialize mock traffic lights"""
        self.traffic_lights = [
            {
                'id': 'tl_001',
                'position': {'lat': 48.8566, 'lng': 2.3525},
                'state': 'GGGrrr',
                'currentPhase': 0,
                'phases': [
                    {'duration': 30, 'state': 'GGGrrr'},
                    {'duration': 5, 'state': 'yyyrrr'},
                    {'duration': 30, 'state': 'rrrGGG'},
                    {'duration': 5, 'state': 'rrryyy'},
                ],
                'lastChange': time.time(),
                'efficiency': 0.85
            },
            {
                'id': 'tl_002',
                'position': {'lat': 48.8560, 'lng': 2.3530},
                'state': 'rrrGGG',
                'currentPhase': 2,
                'phases': [
                    {'duration': 25, 'state': 'rrrGGG'},
                    {'duration': 5, 'state': 'rrryyy'},
                    {'duration': 25, 'state': 'GGGrrr'},
                    {'duration': 5, 'state': 'yyyrrr'},
                ],
                'lastChange': time.time(),
                'efficiency': 0.78
            },
            {
                'id': 'tl_003',
                'position': {'lat': 48.8555, 'lng': 2.3515},
                'state': 'GGrrGG',
                'currentPhase': 0,
                'phases': [
                    {'duration': 20, 'state': 'GGrrGG'},
                    {'duration': 5, 'state': 'yyrryy'},
                    {'duration': 20, 'state': 'rrGGrr'},
                    {'duration': 5, 'state': 'rryyrr'},
                ],
                'lastChange': time.time(),
                'efficiency': 0.92
            }
        ]
    
    def _initialize_network_edges(self):
        """Initialize network edges for vehicle movement"""
        self.edges = [
            {'id': 'edge_1', 'from_lat': 48.8500, 'from_lng': 2.3500, 'to_lat': 48.8510, 'to_lng': 2.3510, 'length': 1.0},
            {'id': 'edge_2', 'from_lat': 48.8510, 'from_lng': 2.3510, 'to_lat': 48.8520, 'to_lng': 2.3520, 'length': 1.0},
            {'id': 'edge_3', 'from_lat': 48.8520, 'from_lng': 2.3520, 'to_lat': 48.8530, 'to_lng': 2.3530, 'length': 1.0},
            {'id': 'edge_4', 'from_lat': 48.8530, 'from_lng': 2.3530, 'to_lat': 48.8540, 'to_lng': 2.3540, 'length': 1.0},
            {'id': 'edge_5', 'from_lat': 48.8540, 'from_lng': 2.3540, 'to_lat': 48.8550, 'to_lng': 2.3550, 'length': 1.0},
        ]
    
    def start_simulation(self, scenario_id: str = 'default'):
        """Start simulation with given scenario"""
        self.current_scenario = scenario_id
        self.is_running = True
        self.is_paused = False
        self.simulation_time = 0
        self.start_real_time = time.time()
        
        # Generate initial vehicles based on scenario
        vehicle_count = self._get_vehicle_count_for_scenario(scenario_id)
        self._generate_initial_vehicles(vehicle_count)
        
        print(f"✅ Simulation started with scenario: {scenario_id}")
        print(f"   Vehicles: {vehicle_count}")
        
        return True
    
    def stop_simulation(self):
        """Stop simulation"""
        self.is_running = False
        self.is_paused = False
        self.vehicles.clear()
        self.simulation_time = 0
        print("⏹️ Simulation stopped")
        
        return True
    
    def pause_simulation(self):
        """Pause simulation"""
        self.is_paused = True
        print("⏸️ Simulation paused")
        
        return True
    
    def resume_simulation(self):
        """Resume simulation"""
        self.is_paused = False
        print("▶️ Simulation resumed")
        
        return True
    
    def _get_vehicle_count_for_scenario(self, scenario_id: str) -> int:
        """Get vehicle count based on scenario"""
        scenario_counts = {
            'default': 50,
            'rush_hour': 120,
            'emergency_test': 30,
            'weekend': 25
        }
        return scenario_counts.get(scenario_id, 50)
    
    def _generate_initial_vehicles(self, count: int):
        """Generate initial vehicles"""
        self.vehicles = []
        vehicle_types = ['passenger', 'bus', 'truck', 'motorcycle', 'bicycle']
        colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4']
        
        for i in range(count):
            vehicle_type = random.choice(vehicle_types)
            color = colors[i % len(colors)]
            
            # Choose random edge
            edge = random.choice(self.edges)
            
            # Interpolate position along edge
            progress = random.random()
            lat = edge['from_lat'] + (edge['to_lat'] - edge['from_lat']) * progress
            lng = edge['from_lng'] + (edge['to_lng'] - edge['from_lng']) * progress
            
            # Set speed based on vehicle type
            speed_ranges = {
                'passenger': (30, 60),
                'bus': (20, 40),
                'truck': (30, 70),
                'motorcycle': (40, 80),
                'bicycle': (15, 25),
                'emergency': (60, 90)
            }
            min_speed, max_speed = speed_ranges.get(vehicle_type, (30, 60))
            
            vehicle = {
                'id': f'veh_{i:03d}',
                'type': vehicle_type,
                'position': {'lat': lat, 'lng': lng},
                'speed': round(random.uniform(min_speed, max_speed), 1),
                'lane': f'{edge["id"]}_lane_{random.randint(0, 1)}',
                'route': [edge['id']] + [e['id'] for e in random.sample(self.edges, 2)],
                'color': color,
                'heading': random.uniform(0, 360),
                'edge': edge['id'],
                'progress': progress,
                'direction': 1 if random.random() > 0.5 else -1,
                'distanceTraveled': 0,
                'createdAt': time.time()
            }
            self.vehicles.append(vehicle)
            self.stats['total_vehicles_created'] += 1
    
    def update_simulation(self, delta_time: float = 0.1):
        """Update simulation by one time step"""
        if not self.is_running or self.is_paused:
            return
        
        self.simulation_time += delta_time
        
        # Update traffic lights
        self._update_traffic_lights(delta_time)
        
        # Update vehicle positions
        self._update_vehicles(delta_time)
        
        # Randomly add/remove vehicles
        self._manage_vehicle_population()
        
        # Calculate metrics
        self.metrics = self.calculate_metrics()
    
    def _update_traffic_lights(self, delta_time: float):
        """Update traffic light states"""
        current_time = time.time()
        
        for tl in self.traffic_lights:
            phase = tl['phases'][tl['currentPhase']]
            
            # Check if phase duration has elapsed
            if current_time - tl.get('lastChange', 0) > phase['duration']:
                tl['currentPhase'] = (tl['currentPhase'] + 1) % len(tl['phases'])
                tl['state'] = tl['phases'][tl['currentPhase']]['state']
                tl['lastChange'] = current_time
    
    def _update_vehicles(self, delta_time: float):
        """Update vehicle positions and speeds"""
        for vehicle in self.vehicles:
            # Check if vehicle is at traffic light
            near_traffic_light = self._is_near_traffic_light(vehicle)
            
            # Adjust speed based on traffic light
            if near_traffic_light and near_traffic_light['state'][0] == 'r':  # Red light
                vehicle['speed'] = max(0, vehicle['speed'] - 20 * delta_time)  # Decelerate
            else:
                # Normal speed with some variation
                base_speed = 50 if vehicle['type'] != 'emergency' else 70
                target_speed = base_speed + random.uniform(-10, 10)
                vehicle['speed'] += (target_speed - vehicle['speed']) * 0.1
            
            # Update progress along edge
            speed_mps = vehicle['speed'] / 3.6  # Convert km/h to m/s
            distance = speed_mps * delta_time
            progress_delta = distance / 1000  # Convert to km progress
            
            vehicle['progress'] += progress_delta * vehicle['direction']
            vehicle['distanceTraveled'] += distance / 1000  # in km
            
            # If vehicle reached end of edge, move to next edge
            if vehicle['progress'] > 1.0 or vehicle['progress'] < 0:
                # Get next edge from route
                current_edge_idx = vehicle['route'].index(vehicle['edge']) if vehicle['edge'] in vehicle['route'] else 0
                next_edge_idx = (current_edge_idx + 1) % len(vehicle['route'])
                next_edge_id = vehicle['route'][next_edge_idx]
                
                # Find next edge
                next_edge = next((e for e in self.edges if e['id'] == next_edge_id), None)
                
                if next_edge:
                    vehicle['edge'] = next_edge_id
                    vehicle['progress'] = 0 if vehicle['direction'] > 0 else 1.0
                    vehicle['lane'] = f'{next_edge_id}_lane_{random.randint(0, 1)}'
            
            # Update position based on progress
            edge = next((e for e in self.edges if e['id'] == vehicle['edge']), None)
            if edge:
                lat = edge['from_lat'] + (edge['to_lat'] - edge['from_lat']) * vehicle['progress']
                lng = edge['from_lng'] + (edge['to_lng'] - edge['from_lng']) * vehicle['progress']
                vehicle['position'] = {'lat': lat, 'lng': lng}
                
                # Update heading (direction of travel)
                dx = edge['to_lng'] - edge['from_lng']
                dy = edge['to_lat'] - edge['from_lat']
                vehicle['heading'] = (180 / 3.14159) * (3.14159 / 2 - (0 if dx == 0 else (dy / dx) if dx != 0 else 0))
    
    def _is_near_traffic_light(self, vehicle: Dict) -> Dict:
        """Check if vehicle is near a traffic light"""
        for tl in self.traffic_lights:
            # Simple distance check (in reality, use proper distance calculation)
            dist = abs(vehicle['position']['lat'] - tl['position']['lat']) + abs(vehicle['position']['lng'] - tl['position']['lng'])
            if dist < 0.001:  # Within ~100m
                return tl
        return None
    
    def _manage_vehicle_population(self):
        """Randomly add or remove vehicles"""
        # Random chance to add vehicle
        if random.random() < 0.1:  # 10% chance each update
            self._add_random_vehicle()
        
        # Random chance to remove vehicle
        if random.random() < 0.05 and len(self.vehicles) > 10:  # 5% chance, keep at least 10
            vehicle_to_remove = random.choice(self.vehicles)
            self.vehicles.remove(vehicle_to_remove)
    
    def _add_random_vehicle(self):
        """Add a random vehicle to simulation"""
        vehicle_types = ['passenger', 'bus', 'truck', 'motorcycle', 'bicycle']
        if random.random() < 0.1:  # 10% chance for emergency
            vehicle_type = 'emergency'
        else:
            vehicle_type = random.choice(vehicle_types)
        
        colors = {
            'passenger': '#3b82f6',
            'emergency': '#ef4444',
            'bus': '#f59e0b',
            'truck': '#8b5cf6',
            'motorcycle': '#10b981',
            'bicycle': '#06b6d4'
        }
        
        edge = random.choice(self.edges)
        progress = random.random()
        lat = edge['from_lat'] + (edge['to_lat'] - edge['from_lat']) * progress
        lng = edge['from_lng'] + (edge['to_lng'] - edge['from_lng']) * progress
        
        vehicle = {
            'id': f'veh_{self.stats["total_vehicles_created"]:04d}',
            'type': vehicle_type,
            'position': {'lat': lat, 'lng': lng},
            'speed': random.uniform(30, 60),
            'lane': f'{edge["id"]}_lane_{random.randint(0, 1)}',
            'route': [edge['id']] + [e['id'] for e in random.sample(self.edges, 2)],
            'color': colors.get(vehicle_type, '#3b82f6'),
            'heading': random.uniform(0, 360),
            'edge': edge['id'],
            'progress': progress,
            'direction': 1 if random.random() > 0.5 else -1,
            'distanceTraveled': 0,
            'createdAt': time.time()
        }
        
        self.vehicles.append(vehicle)
        self.stats['total_vehicles_created'] += 1
    
    def add_emergency_vehicle(self) -> Dict:
        """Add an emergency vehicle"""
        edge = random.choice(self.edges)
        progress = random.random()
        lat = edge['from_lat'] + (edge['to_lat'] - edge['from_lat']) * progress
        lng = edge['from_lng'] + (edge['to_lng'] - edge['from_lng']) * progress
        
        emergency_types = ['ambulance', 'police', 'fire_truck']
        
        vehicle = {
            'id': f'emergency_{self.stats["total_vehicles_created"]:04d}',
            'type': 'emergency',
            'subtype': random.choice(emergency_types),
            'position': {'lat': lat, 'lng': lng},
            'speed': random.uniform(60, 90),
            'lane': f'{edge["id"]}_lane_{random.randint(0, 1)}',
            'route': [edge['id']] + [e['id'] for e in random.sample(self.edges, 3)],
            'color': '#ef4444',
            'heading': random.uniform(0, 360),
            'edge': edge['id'],
            'progress': progress,
            'direction': 1 if random.random() > 0.5 else -1,
            'distanceTraveled': 0,
            'sirenActive': True,
            'priority': 'highest',
            'createdAt': time.time()
        }
        
        self.vehicles.append(vehicle)
        self.stats['total_vehicles_created'] += 1
        self.stats['emergency_vehicles_served'] += 1
        
        return vehicle
    
    def calculate_metrics(self) -> Dict:
        """Calculate simulation metrics"""
        if not self.vehicles:
            return self._get_default_metrics()
        
        total_vehicles = len(self.vehicles)
        total_speed = sum(v['speed'] for v in self.vehicles)
        avg_speed = total_speed / total_vehicles
        
        # Count vehicle types
        vehicle_counts = {}
        for v in self.vehicles:
            v_type = v['type']
            vehicle_counts[v_type] = vehicle_counts.get(v_type, 0) + 1
        
        # Calculate CO2 emissions (simplified)
        total_distance = sum(v['distanceTraveled'] for v in self.vehicles)
        co2_per_km = {
            'passenger': 120,
            'emergency': 180,
            'bus': 80,
            'truck': 150,
            'motorcycle': 60,
            'bicycle': 0
        }
        
        co2_emissions = 0
        for v in self.vehicles:
            co2_emissions += v['distanceTraveled'] * co2_per_km.get(v['type'], 100)
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'totalVehicles': total_vehicles,
            'avgSpeed': round(avg_speed, 1),
            'avgTravelTime': round(random.uniform(30.0, 90.0), 1),
            'co2Emissions': round(co2_emissions, 1),
            'vehicleCounts': vehicle_counts,
            'emergencyVehiclesActive': vehicle_counts.get('emergency', 0),
            'throughput': round(total_distance * 60),  # km per hour approximation
            'congestionLevel': self._calculate_congestion_level(avg_speed),
            'simulationTime': round(self.simulation_time, 1),
            'totalDistanceTraveled': round(total_distance, 2)
        }
    
    def _calculate_congestion_level(self, avg_speed: float) -> str:
        """Calculate congestion level based on average speed"""
        if avg_speed > 50:
            return 'low'
        elif avg_speed > 30:
            return 'medium'
        else:
            return 'high'
    
    def _get_default_metrics(self) -> Dict:
        """Get default metrics when no vehicles"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'totalVehicles': 0,
            'avgSpeed': 0,
            'avgTravelTime': 0,
            'co2Emissions': 0,
            'vehicleCounts': {},
            'emergencyVehiclesActive': 0,
            'throughput': 0,
            'congestionLevel': 'low',
            'simulationTime': round(self.simulation_time, 1),
            'totalDistanceTraveled': 0
        }
    
    def get_simulation_data(self) -> Dict:
        """Get complete simulation data for WebSocket"""
        return {
            'vehicles': self.vehicles,
            'traffic_lights': self.traffic_lights,
            'metrics': self.metrics,
            'timestamp': time.time(),
            'simulation_time': self.simulation_time,
            'scenario': self.current_scenario,
            'is_running': self.is_running,
            'is_paused': self.is_paused,
            'stats': self.stats
        }
    
    def get_vehicle_by_id(self, vehicle_id: str) -> Dict:
        """Get vehicle by ID"""
        for vehicle in self.vehicles:
            if vehicle['id'] == vehicle_id:
                return vehicle
        return None
    
    def remove_vehicle(self, vehicle_id: str) -> bool:
        """Remove vehicle by ID"""
        for i, vehicle in enumerate(self.vehicles):
            if vehicle['id'] == vehicle_id:
                self.vehicles.pop(i)
                return True
        return False