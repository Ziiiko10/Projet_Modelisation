"""
Simulation API routes
"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import time

simulation_bp = Blueprint('simulation', __name__)

# Simulation state
simulation_state = {
    'status': 'stopped',  # stopped, running, paused
    'current_scenario': None,
    'start_time': None,
    'elapsed_time': 0,
    'total_vehicles': 0,
    'simulation_speed': 1.0
}

@simulation_bp.route('/simulation/status', methods=['GET'])
def get_simulation_status():
    """Get current simulation status"""
    if simulation_state['status'] == 'running' and simulation_state['start_time']:
        elapsed = time.time() - datetime.fromisoformat(simulation_state['start_time']).timestamp()
        simulation_state['elapsed_time'] = elapsed
    
    return jsonify({
        'status': simulation_state['status'],
        'currentScenario': simulation_state['current_scenario'],
        'startTime': simulation_state['start_time'],
        'elapsedTime': round(simulation_state['elapsed_time'], 2),
        'totalVehicles': simulation_state['total_vehicles'],
        'simulationSpeed': simulation_state['simulation_speed'],
        'timestamp': datetime.utcnow().isoformat()
    })

@simulation_bp.route('/simulation/start', methods=['POST'])
def start_simulation():
    """Start simulation"""
    data = request.get_json()
    scenario_id = data.get('scenario_id', 'default')
    simulation_speed = data.get('simulation_speed', 1.0)
    
    simulation_state.update({
        'status': 'running',
        'current_scenario': scenario_id,
        'start_time': datetime.utcnow().isoformat(),
        'elapsed_time': 0,
        'simulation_speed': max(0.1, min(10.0, simulation_speed))  # Clamp between 0.1 and 10
    })
    
    return jsonify({
        'message': f'Simulation started with scenario: {scenario_id}',
        'status': simulation_state['status'],
        'scenario': scenario_id,
        'simulationSpeed': simulation_state['simulation_speed']
    })

@simulation_bp.route('/simulation/pause', methods=['POST'])
def pause_simulation():
    """Pause simulation"""
    simulation_state['status'] = 'paused'
    
    return jsonify({
        'message': 'Simulation paused',
        'status': simulation_state['status']
    })

@simulation_bp.route('/simulation/resume', methods=['POST'])
def resume_simulation():
    """Resume simulation"""
    simulation_state['status'] = 'running'
    
    return jsonify({
        'message': 'Simulation resumed',
        'status': simulation_state['status']
    })

@simulation_bp.route('/simulation/stop', methods=['POST'])
def stop_simulation():
    """Stop simulation"""
    simulation_state.update({
        'status': 'stopped',
        'current_scenario': None,
        'start_time': None,
        'elapsed_time': 0
    })
    
    return jsonify({
        'message': 'Simulation stopped',
        'status': simulation_state['status']
    })

@simulation_bp.route('/simulation/reset', methods=['POST'])
def reset_simulation():
    """Reset simulation"""
    simulation_state.update({
        'status': 'stopped',
        'current_scenario': None,
        'start_time': None,
        'elapsed_time': 0,
        'total_vehicles': 0,
        'simulation_speed': 1.0
    })
    
    return jsonify({
        'message': 'Simulation reset',
        'status': simulation_state['status']
    })

@simulation_bp.route('/simulation/speed', methods=['POST'])
def set_simulation_speed():
    """Set simulation speed multiplier"""
    data = request.get_json()
    speed = data.get('speed', 1.0)
    
    # Clamp between 0.1 and 10
    simulation_state['simulation_speed'] = max(0.1, min(10.0, speed))
    
    return jsonify({
        'message': f'Simulation speed set to {simulation_state["simulation_speed"]}x',
        'simulationSpeed': simulation_state['simulation_speed']
    })