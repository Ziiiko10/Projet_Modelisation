"""
Vehicles API routes
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import random
import uuid

vehicles_bp = Blueprint('vehicles', __name__)

# In-memory storage for active vehicles
active_vehicles = {}
vehicle_types = ['passenger', 'emergency', 'bus', 'truck', 'motorcycle', 'bicycle']
vehicle_colors = {
    'passenger': '#3b82f6',  # blue
    'emergency': '#ef4444',  # red
    'bus': '#f59e0b',        # orange
    'truck': '#8b5cf6',      # purple
    'motorcycle': '#10b981', # green
    'bicycle': '#06b6d4'     # cyan
}

@vehicles_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    """Get all active vehicles"""
    limit = request.args.get('limit', type=int)
    
    vehicles_list = list(active_vehicles.values())
    
    if limit:
        vehicles_list = vehicles_list[:limit]
    
    return jsonify({
        'vehicles': vehicles_list,
        'count': len(vehicles_list),
        'timestamp': datetime.utcnow().isoformat()
    })

@vehicles_bp.route('/vehicles/types', methods=['GET'])
def get_vehicle_types():
    """Get available vehicle types"""
    return jsonify({
        'types': [
            {
                'id': 'passenger',
                'name': 'Voiture particulière',
                'description': 'Véhicule de tourisme standard',
                'color': '#3b82f6',
                'avgSpeed': '40-60 km/h'
            },
            {
                'id': 'emergency',
                'name': 'Véhicule d\'urgence',
                'description': 'Ambulance, police, pompiers',
                'color': '#ef4444',
                'avgSpeed': '60-90 km/h'
            },
            {
                'id': 'bus',
                'name': 'Bus',
                'description': 'Transport en commun',
                'color': '#f59e0b',
                'avgSpeed': '30-50 km/h'
            },
            {
                'id': 'truck',
                'name': 'Camion',
                'description': 'Véhicule de marchandises',
                'color': '#8b5cf6',
                'avgSpeed': '30-70 km/h'
            },
            {
                'id': 'motorcycle',
                'name': 'Moto',
                'description': 'Deux-roues motorisé',
                'color': '#10b981',
                'avgSpeed': '40-80 km/h'
            },
            {
                'id': 'bicycle',
                'name': 'Vélo',
                'description': 'Vélo ou vélo électrique',
                'color': '#06b6d4',
                'avgSpeed': '15-25 km/h'
            }
        ]
    })

@vehicles_bp.route('/vehicles/emergency', methods=['POST'])
def add_emergency_vehicle():
    """Add an emergency vehicle to simulation"""
    data = request.get_json()
    
    # Generate vehicle ID
    vehicle_id = f"emergency_{uuid.uuid4().hex[:8]}"
    
    # Emergency vehicle subtypes
    emergency_types = ['ambulance', 'police', 'fire_truck']
    selected_type = random.choice(emergency_types)
    
    # Create emergency vehicle
    vehicle = {
        'id': vehicle_id,
        'type': 'emergency',
        'subtype': selected_type,
        'position': {
            'lat': round(random.uniform(48.850, 48.860), 6),
            'lng': round(random.uniform(2.350, 2.360), 6)
        },
        'speed': round(random.uniform(60.0, 90.0), 1),  # Faster than normal
        'lane': f'edge_{random.randint(1, 5)}_lane_{random.randint(0, 1)}',
        'route': [f'edge_{i}' for i in random.sample(range(1, 6), 3)],
        'color': '#ef4444',  # Red color for emergency
        'heading': random.uniform(0, 360),
        'sirenActive': True,
        'priority': 'highest',
        'destination': random.choice(['Hospital Central', 'Station de police', 'Caserne de pompiers']),
        'createdAt': datetime.utcnow().isoformat(),
        'status': 'active'
    }
    
    # Add to active vehicles
    active_vehicles[vehicle_id] = vehicle
    
    return jsonify({
        'message': 'Emergency vehicle added',
        'vehicle': vehicle,
        'vehicleId': vehicle_id
    }), 201

@vehicles_bp.route('/vehicles/add', methods=['POST'])
def add_vehicle():
    """Add a vehicle to simulation"""
    data = request.get_json()
    
    # Validate vehicle type
    vehicle_type = data.get('type', 'passenger')
    if vehicle_type not in vehicle_types:
        return jsonify({'error': f'Invalid vehicle type. Must be one of: {", ".join(vehicle_types)}'}), 400
    
    # Generate vehicle ID
    vehicle_id = f"{vehicle_type}_{uuid.uuid4().hex[:8]}"
    
    # Create vehicle
    vehicle = {
        'id': vehicle_id,
        'type': vehicle_type,
        'position': data.get('position', {
            'lat': round(random.uniform(48.850, 48.860), 6),
            'lng': round(random.uniform(2.350, 2.360), 6)
        }),
        'speed': data.get('speed', round(random.uniform(20.0, 60.0), 1)),
        'lane': data.get('lane', f'edge_{random.randint(1, 5)}_lane_{random.randint(0, 1)}'),
        'route': data.get('route', [f'edge_{i}' for i in random.sample(range(1, 6), 3)]),
        'color': vehicle_colors.get(vehicle_type, '#3b82f6'),
        'heading': data.get('heading', random.uniform(0, 360)),
        'createdAt': datetime.utcnow().isoformat(),
        'status': 'active'
    }
    
    # Add to active vehicles
    active_vehicles[vehicle_id] = vehicle
    
    return jsonify({
        'message': f'{vehicle_type} vehicle added',
        'vehicle': vehicle,
        'vehicleId': vehicle_id
    }), 201

@vehicles_bp.route('/vehicles/<vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get specific vehicle"""
    if vehicle_id not in active_vehicles:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    return jsonify(active_vehicles[vehicle_id])

@vehicles_bp.route('/vehicles/<vehicle_id>', methods=['DELETE'])
def remove_vehicle(vehicle_id):
    """Remove a vehicle from simulation"""
    if vehicle_id not in active_vehicles:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    removed_vehicle = active_vehicles.pop(vehicle_id)
    
    return jsonify({
        'message': 'Vehicle removed',
        'vehicleId': vehicle_id,
        'vehicle': removed_vehicle
    })

@vehicles_bp.route('/vehicles/<vehicle_id>/update', methods=['PUT'])
def update_vehicle(vehicle_id):
    """Update vehicle data"""
    if vehicle_id not in active_vehicles:
        return jsonify({'error': 'Vehicle not found'}), 404
    
    data = request.get_json()
    vehicle = active_vehicles[vehicle_id]
    
    # Update allowed fields
    if 'position' in data:
        vehicle['position'] = data['position']
    if 'speed' in data:
        vehicle['speed'] = data['speed']
    if 'lane' in data:
        vehicle['lane'] = data['lane']
    if 'route' in data:
        vehicle['route'] = data['route']
    if 'heading' in data:
        vehicle['heading'] = data['heading']
    
    vehicle['updatedAt'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'message': 'Vehicle updated',
        'vehicle': vehicle
    })

@vehicles_bp.route('/vehicles/count', methods=['GET'])
def get_vehicle_count():
    """Get vehicle count by type"""
    counts = {}
    for vehicle_type in vehicle_types:
        counts[vehicle_type] = sum(1 for v in active_vehicles.values() if v['type'] == vehicle_type)
    
    return jsonify({
        'total': len(active_vehicles),
        'byType': counts,
        'timestamp': datetime.utcnow().isoformat()
    })