"""
Metrics API routes
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random
import json

metrics_bp = Blueprint('metrics', __name__)

# Store metrics history
metrics_history = []

@metrics_bp.route('/metrics', methods=['GET'])
def get_current_metrics():
    """Get current simulation metrics"""
    timestamp = datetime.utcnow()
    
    # Generate realistic mock metrics
    metrics = {
        'timestamp': timestamp.isoformat(),
        'totalVehicles': random.randint(80, 250),
        'avgSpeed': round(random.uniform(30.0, 60.0), 1),
        'avgTravelTime': round(random.uniform(50.0, 120.0), 1),
        'co2Emissions': round(random.uniform(80.0, 200.0), 1),
        'queueLengths': {
            'intersection_1': random.randint(0, 15),
            'intersection_2': random.randint(0, 20),
            'intersection_3': random.randint(0, 10),
            'intersection_4': random.randint(0, 12)
        },
        'emergencyVehiclesActive': random.randint(0, 3),
        'throughput': random.randint(600, 1200),
        'congestionLevel': random.choice(['low', 'medium', 'high']),
        'accidentsReported': random.randint(0, 2),
        'trafficLights': random.randint(3, 8),
        'networkEfficiency': round(random.uniform(65.0, 95.0), 1)
    }
    
    # Store in history
    metrics_history.append(metrics)
    
    # Keep only last 1000 entries
    if len(metrics_history) > 1000:
        metrics_history.pop(0)
    
    return jsonify(metrics)

@metrics_bp.route('/metrics/history', methods=['GET'])
def get_metrics_history():
    """Get metrics history"""
    limit = request.args.get('limit', type=int, default=100)
    
    # Return most recent metrics
    history = metrics_history[-limit:] if metrics_history else []
    
    return jsonify({
        'count': len(history),
        'metrics': history,
        'timestamp': datetime.utcnow().isoformat()
    })

@metrics_bp.route('/metrics/summary', methods=['GET'])
def get_metrics_summary():
    """Get metrics summary for dashboard"""
    if not metrics_history:
        return jsonify({'error': 'No metrics data available'}), 404
    
    recent_metrics = metrics_history[-10:]  # Last 10 data points
    
    # Calculate averages
    avg_speed = sum(m.get('avgSpeed', 0) for m in recent_metrics) / len(recent_metrics)
    avg_vehicles = sum(m.get('totalVehicles', 0) for m in recent_metrics) / len(recent_metrics)
    avg_emissions = sum(m.get('co2Emissions', 0) for m in recent_metrics) / len(recent_metrics)
    
    # Count congestion levels
    congestion_counts = {'low': 0, 'medium': 0, 'high': 0}
    for m in recent_metrics:
        level = m.get('congestionLevel', 'low')
        if level in congestion_counts:
            congestion_counts[level] += 1
    
    summary = {
        'timestamp': datetime.utcnow().isoformat(),
        'averageSpeed': round(avg_speed, 1),
        'averageVehicles': round(avg_vehicles),
        'averageEmissions': round(avg_emissions, 1),
        'congestionDistribution': congestion_counts,
        'totalDataPoints': len(metrics_history),
        'timeRange': {
            'start': metrics_history[0]['timestamp'] if metrics_history else None,
            'end': metrics_history[-1]['timestamp'] if metrics_history else None
        }
    }
    
    return jsonify(summary)

@metrics_bp.route('/metrics/export', methods=['GET'])
def export_metrics():
    """Export metrics data in JSON format"""
    format_type = request.args.get('format', 'json')
    
    if format_type == 'csv':
        # Simple CSV conversion
        csv_data = "timestamp,totalVehicles,avgSpeed,avgTravelTime,co2Emissions,throughput,congestionLevel\n"
        for metric in metrics_history[-100:]:  # Last 100 entries
            csv_data += f"{metric['timestamp']},{metric['totalVehicles']},{metric['avgSpeed']},{metric['avgTravelTime']},{metric['co2Emissions']},{metric['throughput']},{metric['congestionLevel']}\n"
        
        return csv_data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=metrics_export.csv'}
    
    else:  # JSON format
        export_data = {
            'exportedAt': datetime.utcnow().isoformat(),
            'totalMetrics': len(metrics_history),
            'format': 'json',
            'data': metrics_history[-100:]  # Last 100 entries
        }
        
        return jsonify(export_data)

@metrics_bp.route('/metrics/traffic-lights', methods=['GET'])
def get_traffic_light_metrics():
    """Get traffic light specific metrics"""
    metrics = []
    
    for i in range(1, 6):  # 5 traffic lights
        light_metrics = {
            'id': f'tl_{i:03d}',
            'position': {
                'lat': 48.8560 + (i * 0.0005),
                'lng': 2.3520 + (i * 0.0005)
            },
            'state': random.choice(['GGGrrr', 'yyyrrr', 'rrrGGG', 'rrryyy']),
            'phase': random.randint(0, 3),
            'queueLength': random.randint(0, 15),
            'throughput': random.randint(50, 200),
            'averageWaitTime': round(random.uniform(10.0, 60.0), 1),
            'lastCycleTime': random.randint(60, 120)
        }
        metrics.append(light_metrics)
    
    return jsonify({
        'trafficLights': metrics,
        'timestamp': datetime.utcnow().isoformat()
    })