import time
import random
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class MockSimulator:
    """Simulateur mock pour le développement frontend"""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.current_scenario = None
        self.simulation_time = 0
        self.vehicles = []
        self.traffic_lights = []
        self.metrics = {}
        
        # Configuration par défaut
        self.vehicle_count = 50
        self.simulation_speed = 1.0  # Multiplicateur de vitesse
        
        # Initialiser les données mock
        self._initialize_mock_data()
        
    def _initialize_mock_data(self):
        """Initialiser les données mockées"""
        # Créer des feux tricolores mock
        self.traffic_lights = [
            {
                'id': f'tl_{i}',
                'position': {'lat': 48.8566 + random.uniform(-0.01, 0.01), 
                            'lng': 2.3522 + random.uniform(-0.01, 0.01)},
                'state': random.choice(['GGGrrr', 'rrrGGG']),
                'currentPhase': 0
            }
            for i in range(4)
        ]
        
        # Créer des véhicules initiaux
        self.vehicles = [
            {
                'id': f'veh_{i}',
                'type': random.choice(['passenger', 'bus', 'truck']),
                'position': {'lat': 48.8566 + random.uniform(-0.02, 0.02),
                            'lng': 2.3522 + random.uniform(-0.02, 0.02)},
                'speed': random.uniform(30, 60),
                'lane': f'lane_{random.randint(1, 4)}',
                'heading': random.uniform(0, 360),
                'color': self._get_vehicle_color(i)
            }
            for i in range(self.vehicle_count)
        ]
        
    def _get_vehicle_color(self, index: int) -> str:
        """Obtenir une couleur basée sur le type de véhicule"""
        colors = ['#3b82f6', '#ef4444', '#10b981', '#8b5cf6']
        return colors[index % len(colors)]
        
    def start_simulation(self, scenario_id: str = 'default') -> bool:
        """Démarrer la simulation"""
        logger.info(f"Démarrage de la simulation avec scénario: {scenario_id}")
        
        if self.is_running:
            logger.warning("Simulation déjà en cours")
            return False
            
        self.current_scenario = scenario_id
        self.is_running = True
        self.is_paused = False
        self.simulation_time = 0
        
        # Ajuster le nombre de véhicules selon le scénario
        if scenario_id == 'rush_hour':
            self.vehicle_count = 150
        elif scenario_id == 'emergency':
            self.vehicle_count = 80
        else:
            self.vehicle_count = 50
            
        self._initialize_mock_data()
        return True
        
    def stop_simulation(self) -> bool:
        """Arrêter la simulation"""
        logger.info("Arrêt de la simulation")
        self.is_running = False
        self.is_paused = False
        return True
        
    def update_simulation(self, delta_time: float):
        """Mettre à jour la simulation"""
        if not self.is_running or self.is_paused:
            return
            
        self.simulation_time += delta_time * self.simulation_speed
        
        # Mettre à jour les positions des véhicules
        for vehicle in self.vehicles:
            # Simulation simple de mouvement
            vehicle['position']['lat'] += random.uniform(-0.0001, 0.0001) * vehicle['speed']
            vehicle['position']['lng'] += random.uniform(-0.0001, 0.0001) * vehicle['speed']
            
            # Garder dans les limites
            vehicle['position']['lat'] = max(48.84, min(48.87, vehicle['position']['lat']))
            vehicle['position']['lng'] = max(2.34, min(2.37, vehicle['position']['lng']))
            
            # Changer la direction aléatoirement
            if random.random() < 0.01:
                vehicle['heading'] = random.uniform(0, 360)
                
        # Mettre à jour les feux tricolores
        for tl in self.traffic_lights:
            if random.random() < 0.02:  # 2% de chance de changer
                tl['state'] = 'GGGrrr' if tl['state'] == 'rrrGGG' else 'rrrGGG'
                
    def get_simulation_data(self) -> Dict[str, Any]:
        """Obtenir les données actuelles de simulation"""
        # Calculer les métriques
        self.metrics = self._calculate_metrics()
        
        return {
            'vehicles': self.vehicles,
            'traffic_lights': self.traffic_lights,
            'metrics': self.metrics,
            'timestamp': time.time(),
            'simulation_time': self.simulation_time,
            'scenario': self.current_scenario
        }
        
    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculer les métriques de performance"""
        if not self.vehicles:
            return {}
            
        speeds = [v['speed'] for v in self.vehicles]
        
        return {
            'total_vehicles': len(self.vehicles),
            'avg_speed': sum(speeds) / len(speeds),
            'avg_travel_time': random.uniform(60, 120),
            'co2_emissions': random.uniform(100, 200),
            'emergency_vehicles': sum(1 for v in self.vehicles if v['type'] == 'emergency'),
            'queue_lengths': {f'intersection_{i}': random.randint(0, 15) for i in range(4)}
        }
        
    def add_emergency_vehicle(self):
        """Ajouter un véhicule d'urgence"""
        emergency_vehicle = {
            'id': f'emergency_{len(self.vehicles)}',
            'type': 'emergency',
            'position': {'lat': 48.8566, 'lng': 2.3522},
            'speed': 80.0,
            'lane': 'emergency_lane',
            'heading': 0,
            'color': '#ef4444'
        }
        self.vehicles.append(emergency_vehicle)
        
    def cleanup(self):
        """Nettoyage"""
        self.stop_simulation()
        self.vehicles.clear()
        self.traffic_lights.clear()