from flask_socketio import emit, join_room, leave_room
from ..simulation.mock_simulator import MockSimulator

simulator = MockSimulator()
connected_clients = set()

def handle_connect():
    """Nouveau client connecté"""
    client_id = request.sid
    connected_clients.add(client_id)
    print(f"Client connected: {client_id}")
    
    # Envoyer état initial
    emit('connect', {'message': 'Connected to Urban Flow API'})
    emit('simulation_status', {'status': 'stopped'})
    
    if simulator.is_running:
        emit('simulation_status', {'status': 'running'})
        # Envoyer données actuelles
        data = simulator.get_simulation_data()
        emit('simulation_update', data)

def handle_disconnect():
    """Client déconnecté"""
    client_id = request.sid
    connected_clients.remove(client_id)
    print(f"Client disconnected: {client_id}")

def handle_command(data):
    """Commande du client (start, pause, stop, etc.)"""
    command = data.get('command')
    
    if command == 'start':
        scenario_id = data.get('scenario_id', 'default')
        simulator.start_simulation(scenario_id)
        emit('simulation_status', {'status': 'running'})
        
    elif command == 'pause':
        simulator.is_paused = True
        emit('simulation_status', {'status': 'paused'})
        
    elif command == 'resume':
        simulator.is_paused = False
        emit('simulation_status', {'status': 'running'})
        
    elif command == 'stop':
        simulator.is_running = False
        emit('simulation_status', {'status': 'stopped'})
        
    elif command == 'emergency_vehicle':
        simulator.add_emergency_vehicle()
        emit('notification', {'message': 'Emergency vehicle added'})