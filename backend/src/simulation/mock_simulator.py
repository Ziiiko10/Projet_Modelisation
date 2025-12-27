import time
import random
import math
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MockSimulator:
    """Simulateur mocké pour Urban Flow avec données réalistes"""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.current_scenario = None
        self.simulation_time = 0
        self.simulation_speed = 1.0
        
        # Données de simulation
        self.vehicles = []
        self.traffic_lights = []
        self.metrics = {}
        self.network = []
        
        # Configuration des scénarios
        self.scenarios = {
            'default': {
                'name': 'Trafic Normal',
                'vehicle_count': 50,
                'emergency_vehicles': 1,
                'traffic_density': 0.6,
                'speed_range': (30, 60)
            },
            'rush_hour': {
                'name': 'Heure de Pointe',
                'vehicle_count': 150,
                'emergency_vehicles': 3,
                'traffic_density': 0.9,
                'speed_range': (20, 40)
            },
            'weekend': {
                'name': 'Week-end',
                'vehicle_count': 80,
                'emergency_vehicles': 2,
                'traffic_density': 0.7,
                'speed_range': (40, 70)
            },
            'emergency_test': {
                'name': 'Test Urgence',
                'vehicle_count': 30,
                'emergency_vehicles': 5,
                'traffic_density': 0.4,
                'speed_range': (50, 80)
            }
        }
        
        # Initialisation
        self._initialize_network()
        
    def _initialize_network(self):
        """Initialiser le réseau routier mocké"""
        self.network = []
        
        # Intersections principales
        intersections = [
            {'id': 'int_1', 'position': {'lat': 48.8560, 'lng': 2.3515}},
            {'id': 'int_2', 'position': {'lat': 48.8560, 'lng': 2.3529}},
            {'id': 'int_3', 'position': {'lat': 48.8572, 'lng': 2.3515}},
            {'id': 'int_4', 'position': {'lat': 48.8572, 'lng': 2.3529}},
        ]
        
        # Routes entre intersections
        for i in range(len(intersections)):
            for j in range(i + 1, len(intersections)):
                self.network.append({
                    'id': f'road_{i}_{j}',
                    'from': intersections[i]['id'],
                    'to': intersections[j]['id'],
                    'length': random.uniform(100, 500),
                    'lanes': random.randint(1, 3)
                })
                
    def _initialize_traffic_lights(self):
        """Initialiser les feux tricolores"""
        self.traffic_lights = []
        
        phases = [
            {'duration': 30, 'state': 'GGGrrr'},
            {'duration': 3, 'state': 'yyyrrr'},
            {'duration': 30, 'state': 'rrrGGG'},
            {'duration': 3, 'state': 'rrryyy'},
        ]
        
        for i in range(4):
            self.traffic_lights.append({
                'id': f'tl_{i}',
                'name': f'Feu {i+1}',
                'position': {
                    'lat': 48.8566 + random.uniform(-0.005, 0.005),
                    'lng': 2.3522 + random.uniform(-0.005, 0.005)
                },
                'state': random.choice(['GGGrrr', 'rrrGGG']),
                'currentPhase': 0,
                'phases': phases,
                'phaseStartTime': time.time(),
                'intersectionId': f'int_{i+1}'
            })
            
    def _generate_vehicles(self, scenario_config: Dict):
        """Générer des véhicules pour un scénario"""
        vehicle_types = ['passenger', 'bus', 'truck', 'motorcycle', 'emergency']
        type_weights = [0.7, 0.1, 0.1, 0.08, 0.02]
        
        self.vehicles = []
        
        for i in range(scenario_config['vehicle_count']):
            vehicle_type = random.choices(vehicle_types, weights=type_weights)[0]
            road = random.choice(self.network)
            
            self.vehicles.append({
                'id': f'veh_{vehicle_type}_{i}',
                'type': vehicle_type,
                'position': {
                    'lat': 48.8566 + random.uniform(-0.01, 0.01),
                    'lng': 2.3522 + random.uniform(-0.01, 0.01)
                },
                'speed': random.uniform(*scenario_config['speed_range']),
                'lane': f'lane_{random.randint(1, 3)}',
                'heading': random.uniform(0, 360),
                'route': [road['from'], road['to']],
                'color': self._get_vehicle_color(vehicle_type),
                'length': self._get_vehicle_length(vehicle_type),
                'acceleration': 0,
                'waitingTime': 0,
                'distanceTraveled': 0
            })
            
    def _get_vehicle_color(self, vehicle_type: str) -> str:
        """Obtenir la couleur d'un véhicule"""
        colors = {
            'passenger': '#3b82f6',
            'emergency': '#ef4444',
            'bus': '#10b981',
            'truck': '#8b5cf6',
            'motorcycle': '#f59e0b'
        }
        return colors.get(vehicle_type, '#6b7280')
        
    def _get_vehicle_length(self, vehicle_type: str) -> float:
        """Obtenir la longueur d'un véhicule"""
        lengths = {
            'passenger': 4.5,
            'emergency': 6.0,
            'bus': 12.0,
            'truck': 18.0,
            'motorcycle': 2.0
        }
        return lengths.get(vehicle_type, 4.5)
        
    def start_simulation(self, scenario_id: str = 'default', speed: float = 1.0) -> bool:
        """Démarrer la simulation"""
        if scenario_id not in self.scenarios:
            logger.error(f"Scénario inconnu: {scenario_id}")
            return False
            
        logger.info(f"Démarrage simulation: {scenario_id}")
        
        if self.is_running:
            self.stop_simulation()
            time.sleep(0.1)
            
        self.current_scenario = scenario_id
        self.simulation_speed = max(0.1, min(10.0, speed))
        self.simulation_time = 0
        self.is_running = True
        self.is_paused = False
        
        self._initialize_traffic_lights()
        self._generate_vehicles(self.scenarios[scenario_id])
        
        emergency_count = self.scenarios[scenario_id]['emergency_vehicles']
        for i in range(emergency_count):
            self.add_emergency_vehicle()
            
        logger.info(f"Simulation démarrée: {len(self.vehicles)} véhicules")
        return True
        
    def stop_simulation(self) -> bool:
        """Arrêter la simulation"""
        logger.info("Arrêt simulation")
        self.is_running = False
        self.is_paused = False
        self.current_scenario = None
        return True
        
    def update_simulation(self, delta_time: float):
        """Mettre à jour la simulation"""
        if not self.is_running or self.is_paused:
            return
            
        dt = delta_time * self.simulation_speed
        self.simulation_time += dt
        
        self._update_traffic_lights(dt)
        self._update_vehicles(dt)
        
    def _update_traffic_lights(self, delta_time: float):
        """Mettre à jour les feux"""
        current_time = time.time()
        
        for tl in self.traffic_lights:
            phase_duration = tl['phases'][tl['currentPhase']]['duration']
            elapsed = current_time - tl['phaseStartTime']
            
            if elapsed >= phase_duration:
                tl['currentPhase'] = (tl['currentPhase'] + 1) % len(tl['phases'])
                tl['phaseStartTime'] = current_time
                tl['state'] = tl['phases'][tl['currentPhase']]['state']
                
    def _update_vehicles(self, delta_time: float):
        """Mettre à jour les positions des véhicules"""
        for vehicle in self.vehicles:
            speed_ms = vehicle['speed'] / 3.6
            distance = speed_ms * delta_time
            
            angle_rad = math.radians(vehicle['heading'])
            lat_change = (distance * math.cos(angle_rad)) / 111000
            lng_change = (distance * math.sin(angle_rad)) / (111000 * math.cos(math.radians(vehicle['position']['lat'])))
            
            vehicle['position']['lat'] += lat_change
            vehicle['position']['lng'] += lng_change
            vehicle['distanceTraveled'] += distance
            
            # Vérifier les limites
            if not (48.855 < vehicle['position']['lat'] < 48.858):
                vehicle['heading'] = (vehicle['heading'] + 180) % 360
                
            if not (2.351 < vehicle['position']['lng'] < 2.3535):
                vehicle['heading'] = (vehicle['heading'] + 180) % 360
                
            if random.random() < 0.05:
                vehicle['speed'] = max(5, vehicle['speed'] * random.uniform(0.7, 0.9))
                vehicle['waitingTime'] += delta_time
            else:
                target_speed = random.uniform(40, 60)
                if vehicle['speed'] < target_speed:
                    vehicle['speed'] = min(target_speed, vehicle['speed'] + 2 * delta_time)
                    
            if random.random() < 0.01:
                vehicle['heading'] = (vehicle['heading'] + random.uniform(-30, 30)) % 360
                
    def get_simulation_data(self) -> Dict[str, Any]:
        """Obtenir les données complètes de simulation"""
        return {
            'vehicles': self.vehicles,
            'traffic_lights': self.traffic_lights,
            'metrics': self.calculate_metrics(),
            'timestamp': time.time(),
            'simulation_time': self.simulation_time,
            'scenario': self.current_scenario,
            'network': self.network
        }
        
    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculer les métriques"""
        if not self.vehicles:
            return {}
            
        speeds = [v['speed'] for v in self.vehicles]
        waiting_times = [v.get('waitingTime', 0) for v in self.vehicles]
        vehicle_types = [v['type'] for v in self.vehicles]
        
        type_counts = {}
        for vtype in vehicle_types:
            type_counts[vtype] = type_counts.get(vtype, 0) + 1
            
        total_co2 = sum(v['distanceTraveled'] * 0.12 for v in self.vehicles)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'totalVehicles': len(self.vehicles),
            'avgSpeed': sum(speeds) / len(speeds),
            'maxSpeed': max(speeds) if speeds else 0,
            'minSpeed': min(speeds) if speeds else 0,
            'avgTravelTime': self.simulation_time,
            'avgWaitingTime': sum(waiting_times) / len(waiting_times) if waiting_times else 0,
            'co2Emissions': total_co2,
            'vehicleTypeCounts': type_counts,
            'emergencyVehiclesActive': type_counts.get('emergency', 0),
            'queueLengths': {f'intersection_{i}': random.randint(0, 10) for i in range(4)},
            'throughput': len(self.vehicles) * 3600 / max(1, self.simulation_time)
        }
        
    def add_emergency_vehicle(self, vehicle_data: Optional[Dict] = None) -> str:
        """Ajouter un véhicule d'urgence"""
        emergency_id = f'emergency_{int(time.time())}_{len(self.vehicles)}'
        
        vehicle = vehicle_data or {}
        self.vehicles.append({
            'id': emergency_id,
            'type': 'emergency',
            'position': vehicle.get('position', {
                'lat': 48.8566,
                'lng': 2.3522
            }),
            'speed': vehicle.get('speed', 80.0),
            'lane': 'emergency_lane',
            'heading': vehicle.get('heading', 0),
            'route': ['emergency_start', 'emergency_end'],
            'color': '#ef4444',
            'length': 6.0,
            'acceleration': 0,
            'waitingTime': 0,
            'distanceTraveled': 0,
            'sirenActive': True
        })
        
        logger.info(f"Véhicule d'urgence ajouté: {emergency_id}")
        return emergency_id
        
    def cleanup(self):
        """Nettoyer les ressources"""
        self.stop_simulation()
        self.vehicles.clear()
        self.traffic_lights.clear()
        self.network.clear()
        logger.info("Simulateur nettoyé")