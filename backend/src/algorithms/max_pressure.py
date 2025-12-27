"""
Maximum Pressure algorithm for traffic signal control
"""
import time
from typing import Dict, List, Any

class MaxPressureAlgorithm:
    """
    Implements Maximum Pressure algorithm for adaptive traffic signal control
    """
    
    def __init__(self):
        self.name = "Max Pressure Algorithm"
        self.description = "Adaptive traffic signal control based on queue pressures"
        self.pressure_history = {}
        self.learning_rate = 0.1
    
    def calculate_pressure(self, lanes_data: List[Dict]) -> Dict[str, float]:
        """
        Calculate pressure for each approach
        """
        pressures = {}
        
        for lane in lanes_data:
            lane_id = lane['id']
            queue_length = lane.get('queue_length', 0)
            arrival_rate = lane.get('arrival_rate', 0)
            saturation_flow = lane.get('saturation_flow', 1800)  # vehicles/hour
            
            # Pressure calculation
            pressure = queue_length * arrival_rate / max(saturation_flow, 1)
            pressures[lane_id] = pressure
            
            # Store in history
            if lane_id not in self.pressure_history:
                self.pressure_history[lane_id] = []
            self.pressure_history[lane_id].append({
                'pressure': pressure,
                'timestamp': time.time()
            })
        
        return pressures
    
    def optimize_signals(self, intersection_data: Dict) -> Dict[str, Any]:
        """
        Optimize traffic signals based on maximum pressure
        """
        intersection_id = intersection_data['id']
        approaches = intersection_data.get('approaches', [])
        
        # Calculate pressures
        pressures = self.calculate_pressure(approaches)
        
        # Find max pressure approach
        max_pressure_lane = max(pressures.items(), key=lambda x: x[1])[0]
        max_pressure = pressures[max_pressure_lane]
        
        # Determine phase duration based on pressure
        base_duration = 30
        if max_pressure > 10:
            duration = min(60, base_duration + int(max_pressure * 2))
        elif max_pressure < 2:
            duration = max(20, base_duration - 10)
        else:
            duration = base_duration
        
        # Create optimized phases
        phases = []
        
        # Phase 1: Serve max pressure approach
        phases.append({
            'id': 'phase_max_pressure',
            'duration': duration,
            'state': self._get_phase_state(max_pressure_lane),
            'served_lanes': [max_pressure_lane],
            'pressure': max_pressure
        })
        
        # Other phases
        for lane_id, pressure in pressures.items():
            if lane_id != max_pressure_lane and pressure > 0:
                phase_duration = min(30, base_duration + int(pressure))
                phases.append({
                    'id': f'phase_{lane_id}',
                    'duration': phase_duration,
                    'state': self._get_phase_state(lane_id),
                    'served_lanes': [lane_id],
                    'pressure': pressure
                })
        
        return {
            'algorithm': self.name,
            'intersection_id': intersection_id,
            'phases': phases,
            'pressures': pressures,
            'max_pressure_lane': max_pressure_lane,
            'cycle_time': sum(p['duration'] for p in phases),
            'timestamp': time.time()
        }
    
    def _get_phase_state(self, lane_id: str) -> str:
        """
        Get traffic light state for a lane
        """
        # Simplified mapping
        if 'north' in lane_id or 'south' in lane_id:
            return 'GGGrrr'
        elif 'east' in lane_id or 'west' in lane_id:
            return 'rrrGGG'
        else:
            return 'GGrrGG'