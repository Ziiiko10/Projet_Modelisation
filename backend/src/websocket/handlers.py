import time
import logging
from flask import request
from flask_socketio import emit

logger = logging.getLogger(__name__)

def setup_socket_handlers(socketio, simulator, simulation_stream):
    """Configurer tous les handlers WebSocket"""
    
    @socketio.on('connect')
    def handle_connect():
        """Nouveau client connecté"""
        client_id = request.sid
        logger.info(f"Client connecté: {client_id}")
        
        emit('connected', {
            'message': 'Connected to Urban Flow Simulation',
            'client_id': client_id,
            'timestamp': time.time(),
            'simulation_status': {
                'running': simulator.is_running,
                'paused': simulator.is_paused,
                'scenario': simulator.current_scenario
            }
        })
        
        if simulator.is_running:
            initial_data = simulator.get_simulation_data()
            emit('simulation_update', initial_data)
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Client déconnecté"""
        client_id = request.sid
        logger.info(f"Client déconnecté: {client_id}")
    
    @socketio.on('command')
    def handle_command(data):
        """Traiter une commande"""
        command = data.get('command')
        logger.info(f"Commande reçue: {command} de {request.sid}")
        
        if command == 'start':
            scenario_id = data.get('scenario_id', 'default')
            speed = data.get('speed', 1.0)
            
            if simulator.start_simulation(scenario_id, speed):
                simulation_stream.start_streaming()
                
                emit('simulation_status', {
                    'status': 'running',
                    'scenario': scenario_id,
                    'speed': speed,
                    'timestamp': time.time()
                }, broadcast=True)
                
                return {'success': True, 'message': f'Simulation démarrée: {scenario_id}'}
            else:
                return {'success': False, 'error': 'Impossible de démarrer'}
                
        elif command == 'pause':
            simulator.is_paused = True
            emit('simulation_status', {
                'status': 'paused',
                'timestamp': time.time()
            }, broadcast=True)
            return {'success': True, 'message': 'Simulation en pause'}
            
        elif command == 'resume':
            simulator.is_paused = False
            emit('simulation_status', {
                'status': 'running',
                'timestamp': time.time()
            }, broadcast=True)
            return {'success': True, 'message': 'Simulation reprise'}
            
        elif command == 'stop':
            simulator.stop_simulation()
            simulation_stream.stop_streaming()
            
            emit('simulation_status', {
                'status': 'stopped',
                'timestamp': time.time()
            }, broadcast=True)
            
            emit('simulation_update', {
                'vehicles': [],
                'traffic_lights': [],
                'metrics': {},
                'timestamp': time.time(),
                'simulation_time': 0
            }, broadcast=True)
            
            return {'success': True, 'message': 'Simulation arrêtée'}
            
        elif command == 'emergency_vehicle':
            try:
                vehicle_data = data.get('vehicle', {})
                emergency_id = simulator.add_emergency_vehicle(vehicle_data)
                
                emit('emergency_vehicle_added', {
                    'vehicle_id': emergency_id,
                    'position': vehicle_data.get('position', {}),
                    'timestamp': time.time()
                }, broadcast=True)
                
                return {'success': True, 'vehicle_id': emergency_id}
                
            except Exception as e:
                logger.error(f"Erreur véhicule d'urgence: {e}")
                return {'success': False, 'error': str(e)}
        
        else:
            return {'success': False, 'error': f'Commande inconnue: {command}'}