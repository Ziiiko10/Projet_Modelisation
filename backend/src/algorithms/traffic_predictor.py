"""
Traffic prediction algorithms
"""
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any

class TrafficPredictor:
    """
    Predicts traffic patterns based on historical data and current conditions
    """
    
    def __init__(self):
        self.historical_data = {}
        self.patterns = {}
    
    def predict_traffic(self, location: str, time_ahead: int = 60) -> Dict:
        """
        Predict traffic conditions for a location
        time_ahead: minutes to predict ahead
        """
        current_time = datetime.now()
        hour = current_time.hour
        
        # Base predictions on time of day
        if 7 <= hour < 9 or 17 <= hour < 19:
            # Rush hour
            prediction = {
                'traffic_level': 'high',
                'predicted_speed': 25,
                'congestion_probability': 0.8,
                'wait_time': 5
            }
        elif 9 <= hour < 17:
            # Daytime
            prediction = {
                'traffic_level': 'medium',
                'predicted_speed': 40,
                'congestion_probability': 0.4,
                'wait_time': 2
            }
        else:
            # Night
            prediction = {
                'traffic_level': 'low',
                'predicted_speed': 55,
                'congestion_probability': 0.1,
                'wait_time': 1
            }
        
        # Adjust based on day of week
        weekday = current_time.weekday()
        if weekday >= 5:  # Weekend
            prediction['traffic_level'] = 'low'
            prediction['predicted_speed'] += 10
            prediction['congestion_probability'] *= 0.5
        
        return {
            'location': location,
            'prediction': prediction,
            'valid_for_minutes': time_ahead,
            'confidence': 0.85,
            'generated_at': current_time.isoformat()
        }
    
    def predict_congestion(self, network_data: Dict) -> List[Dict]:
        """
        Predict congestion points in the network
        """
        predictions = []
        
        # Mock congestion points
        congestion_points = [
            {
                'location': {'lat': 48.8560, 'lng': 2.3520},
                'probability': 0.9,
                'severity': 'high',
                'expected_start': (datetime.now() + timedelta(minutes=5)).isoformat(),
                'expected_duration_min': 30,
                'affected_routes': ['edge_1', 'edge_2']
            },
            {
                'location': {'lat': 48.8565, 'lng': 2.3530},
                'probability': 0.6,
                'severity': 'medium',
                'expected_start': (datetime.now() + timedelta(minutes=15)).isoformat(),
                'expected_duration_min': 20,
                'affected_routes': ['edge_3']
            }
        ]
        
        return congestion_points
    
    def learn_patterns(self, traffic_data: List[Dict]):
        """
        Learn traffic patterns from historical data
        """
        for data_point in traffic_data:
            hour = data_point.get('hour')
            location = data_point.get('location')
            
            if location not in self.patterns:
                self.patterns[location] = {}
            
            if hour not in self.patterns[location]:
                self.patterns[location][hour] = []
            
            self.patterns[location][hour].append({
                'speed': data_point.get('speed'),
                'density': data_point.get('density'),
                'timestamp': data_point.get('timestamp')
            })
    
    def get_pattern_summary(self) -> Dict:
        """
        Get summary of learned traffic patterns
        """
        summary = {}
        
        for location, patterns in self.patterns.items():
            for hour, data_points in patterns.items():
                if data_points:
                    avg_speed = np.mean([dp.get('speed', 0) for dp in data_points])
                    avg_density = np.mean([dp.get('density', 0) for dp in data_points])
                    
                    if location not in summary:
                        summary[location] = {}
                    
                    summary[location][hour] = {
                        'average_speed': avg_speed,
                        'average_density': avg_density,
                        'data_points': len(data_points)
                    }
        
        return summary