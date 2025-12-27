"""
Scenarios API routes
"""
from flask import Blueprint, jsonify, request
from models.scenario import Scenario, db
from models.simulation import db as simulation_db

scenarios_bp = Blueprint('scenarios', __name__)

@scenarios_bp.route('/scenarios', methods=['GET'])
def get_scenarios():
    """Get all scenarios"""
    scenarios = Scenario.query.all()
    
    # If no scenarios exist, create default ones
    if not scenarios:
        default_scenarios = Scenario.get_default_scenarios()
        for scenario in default_scenarios:
            simulation_db.session.add(scenario)
        simulation_db.session.commit()
        scenarios = default_scenarios
    
    return jsonify({
        'scenarios': [scenario.to_dict() for scenario in scenarios],
        'count': len(scenarios)
    })

@scenarios_bp.route('/scenarios', methods=['POST'])
def create_scenario():
    """Create a new scenario"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('id') or not data.get('name'):
        return jsonify({'error': 'id and name are required'}), 400
    
    # Check if scenario already exists
    existing = Scenario.query.get(data['id'])
    if existing:
        return jsonify({'error': f'Scenario with id {data["id"]} already exists'}), 400
    
    # Create new scenario
    scenario = Scenario(
        id=data['id'],
        name=data['name'],
        description=data.get('description', ''),
        vehicle_count=data.get('vehicleCount', 100),
        traffic_density=data.get('trafficDensity', 'medium'),
        has_emergency_vehicles=data.get('hasEmergencyVehicles', False),
        duration=data.get('duration', 3600)
    )
    
    simulation_db.session.add(scenario)
    simulation_db.session.commit()
    
    return jsonify({
        'message': 'Scenario created successfully',
        'scenario': scenario.to_dict()
    }), 201

@scenarios_bp.route('/scenarios/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Get specific scenario"""
    scenario = Scenario.query.get(scenario_id)
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    return jsonify(scenario.to_dict())

@scenarios_bp.route('/scenarios/<scenario_id>', methods=['PUT'])
def update_scenario(scenario_id):
    """Update scenario"""
    scenario = Scenario.query.get(scenario_id)
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        scenario.name = data['name']
    if 'description' in data:
        scenario.description = data['description']
    if 'vehicleCount' in data:
        scenario.vehicle_count = data['vehicleCount']
    if 'trafficDensity' in data:
        scenario.traffic_density = data['trafficDensity']
    if 'hasEmergencyVehicles' in data:
        scenario.has_emergency_vehicles = data['hasEmergencyVehicles']
    if 'duration' in data:
        scenario.duration = data['duration']
    
    simulation_db.session.commit()
    
    return jsonify({
        'message': 'Scenario updated successfully',
        'scenario': scenario.to_dict()
    })

@scenarios_bp.route('/scenarios/<scenario_id>', methods=['DELETE'])
def delete_scenario(scenario_id):
    """Delete scenario"""
    # Don't allow deletion of default scenarios
    default_scenarios = ['default', 'rush_hour', 'emergency_test', 'weekend']
    if scenario_id in default_scenarios:
        return jsonify({'error': 'Cannot delete default scenarios'}), 400
    
    scenario = Scenario.query.get(scenario_id)
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    simulation_db.session.delete(scenario)
    simulation_db.session.commit()
    
    return jsonify({'message': 'Scenario deleted successfully'})

@scenarios_bp.route('/scenarios/<scenario_id>/activate', methods=['POST'])
def activate_scenario(scenario_id):
    """Activate a scenario"""
    scenario = Scenario.query.get(scenario_id)
    
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    # Deactivate all other scenarios
    Scenario.query.update({'is_active': False})
    
    # Activate this scenario
    scenario.is_active = True
    simulation_db.session.commit()
    
    return jsonify({
        'message': f'Scenario {scenario.name} activated',
        'scenario': scenario.to_dict()
    })

@scenarios_bp.route('/scenarios/active', methods=['GET'])
def get_active_scenario():
    """Get currently active scenario"""
    active_scenario = Scenario.query.filter_by(is_active=True).first()
    
    if not active_scenario:
        return jsonify({'message': 'No active scenario'}), 404
    
    return jsonify(active_scenario.to_dict())