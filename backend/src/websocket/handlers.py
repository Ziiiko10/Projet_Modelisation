"""
WebSocket event handlers
"""
import time
from flask import request
from flask_socketio import emit, join_room, leave_room

class WebSocketManager:
    """Manages WebSocket connections and events"""
    
    def __init__(self, socketio, simulator, simulation_stream):
        self.socketio = socketio
        self.simulator = simulator
        self.simulation_stream = simulation_stream
        self.connected_clients = set()
        self.client_info = {}  # Store additional client info
        
        # Register event handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all WebSocket event handlers"""
        @self.socketio.on('connect')
        def handle_connect():
            self.on_connect()
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.on_disconnect()
        
        @self.socketio.on('command')
        def handle_command(data):
            self.on_command(data)
        
        @self.socketio.on('emergency_vehicle')
        def handle_emergency_vehicle(data):
            self.on_emergency_vehicle(data)
        
        @self.socketio.on('change_scenario')
        def handle_change_scenario(data):
            self.on_change_scenario(data)
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            self.on_subscribe(data)
        
        @self.socketio.on('unsubscribe')
        def handle_unsubscribe(data):
            self.on_unsubscribe(data)
    
    def on_connect(self):
        """Handle new client connection"""
        client_id = request.sid
        self.connected_clients.add(client_id)
        
        # Store client info
        self.client_info[client_id] = {
            'connected_at': time.time(),
            'last_activity': time.time(),
            'subscriptions': set(),
            'ip': request.remote_addr
        }
        
        print(f"✅ Client connected: {client_id}")
        
        # Send welcome message
        emit('connect', {
            'message': 'Connected to Urban Flow WebSocket API',
            'client_id': client_id,
            'timestamp': time.time()
        })
        
        # Send current simulation status
        emit('simulation_status', {
            'status': 'running' if self.simulator.is_running else 'stopped',
            'is_paused': self.simulator.is_paused,
            'current_scenario': self.simulator.current_scenario,
            'simulation_time': self.simulator.simulation_time
        })
        
        # If simulation is running, send current data
        if self.simulator.is_running and not self.simulator.is_paused:
            data = self.simulator.get_simulation_data()
            emit('simulation_update', data)
    
    def on_disconnect(self):
        """Handle client disconnection"""
        client_id = request.sid
        
        if client_id in self.connected_clients:
            self.connected_clients.remove(client_id)
        
        if client_id in self.client_info:
            del self.client_info[client_id]
        
        print(f"❌ Client disconnected: {client_id}")
    
    def on_command(self, data):
        """Handle client command"""
        client_id = request.sid
        
        if client_id not in self.connected_clients:
            emit('error', {'message': 'Client not connected'})
            return
        
        command = data.get('command')
        
        if not command:
            emit('error', {'message': 'No command specified'})
            return
        
        print(f"📨 Command from {client_id}: {command}")
        
        try:
            if command == 'start':
                scenario_id = data.get('scenario_id', 'default')
                success = self.simulator.start_simulation(scenario_id)
                
                if success:
                    # Start streaming if not already
                    if not self.simulation_stream.streaming:
                        self.simulation_stream.start_streaming()
                    
                    emit('simulation_status', {
                        'status': 'running',
                        'scenario': scenario_id,
                        'message': f'Simulation started with scenario: {scenario_id}'
                    })
                    
                    # Broadcast to all clients
                    self.socketio.emit('notification', {
                        'type': 'info',
                        'message': f'Simulation started with scenario: {scenario_id}',
                        'timestamp': time.time()
                    })
                else:
                    emit('error', {'message': 'Failed to start simulation'})
            
            elif command == 'pause':
                success = self.simulator.pause_simulation()
                
                if success:
                    emit('simulation_status', {
                        'status': 'paused',
                        'message': 'Simulation paused'
                    })
                else:
                    emit('error', {'message': 'Failed to pause simulation'})
            
            elif command == 'resume':
                success = self.simulator.resume_simulation()
                
                if success:
                    emit('simulation_status', {
                        'status': 'running',
                        'message': 'Simulation resumed'
                    })
                else:
                    emit('error', {'message': 'Failed to resume simulation'})
            
            elif command == 'stop':
                success = self.simulator.stop_simulation()
                
                if success:
                    emit('simulation_status', {
                        'status': 'stopped',
                        'message': 'Simulation stopped'
                    })
                else:
                    emit('error', {'message': 'Failed to stop simulation'})
            
            elif command == 'reset':
                # Stop and reset
                self.simulator.stop_simulation()
                self.simulator.simulation_time = 0
                
                emit('simulation_status', {
                    'status': 'stopped',
                    'message': 'Simulation reset',
                    'simulation_time': 0
                })
            
            elif command == 'speed':
                speed = data.get('speed', 1.0)
                # Note: In mock simulator, speed control would be implemented
                emit('notification', {
                    'type': 'info',
                    'message': f'Simulation speed set to {speed}x',
                    'timestamp': time.time()
                })
            
            elif command == 'get_status':
                # Send current status
                emit('simulation_status', {
                    'status': 'running' if self.simulator.is_running else 'stopped',
                    'is_paused': self.simulator.is_paused,
                    'current_scenario': self.simulator.current_scenario,
                    'simulation_time': self.simulator.simulation_time,
                    'vehicle_count': len(self.simulator.vehicles),
                    'timestamp': time.time()
                })
            
            else:
                emit('error', {'message': f'Unknown command: {command}'})
        
        except Exception as e:
            emit('error', {
                'message': f'Error executing command: {str(e)}'
            })
    
    def on_emergency_vehicle(self, data):
        """Handle emergency vehicle request"""
        client_id = request.sid
        
        if client_id not in self.connected_clients:
            emit('error', {'message': 'Client not connected'})
            return
        
        try:
            # Add emergency vehicle to simulation
            vehicle = self.simulator.add_emergency_vehicle()
            
            if vehicle:
                # Send notification
                emit('notification', {
                    'type': 'emergency',
                    'message': 'Emergency vehicle added to simulation',
                    'vehicle_id': vehicle['id'],
                    'vehicle_type': vehicle.get('subtype', 'emergency'),
                    'timestamp': time.time()
                })
                
                # Broadcast to all clients
                self.socketio.emit('emergency_alert', {
                    'message': 'Emergency vehicle in transit',
                    'vehicle': vehicle,
                    'timestamp': time.time()
                })
            else:
                emit('error', {'message': 'Failed to add emergency vehicle'})
        
        except Exception as e:
            emit('error', {
                'message': f'Error adding emergency vehicle: {str(e)}'
            })
    
    def on_change_scenario(self, data):
        """Handle scenario change request"""
        client_id = request.sid
        
        if client_id not in self.connected_clients:
            emit('error', {'message': 'Client not connected'})
            return
        
        scenario_id = data.get('scenario_id')
        
        if not scenario_id:
            emit('error', {'message': 'No scenario_id specified'})
            return
        
        try:
            # Check if simulation is running
            if self.simulator.is_running:
                # Stop current simulation
                self.simulator.stop_simulation()
                
                # Start new simulation with requested scenario
                success = self.simulator.start_simulation(scenario_id)
                
                if success:
                    emit('simulation_status', {
                        'status': 'running',
                        'scenario': scenario_id,
                        'message': f'Changed to scenario: {scenario_id}'
                    })
                    
                    # Broadcast to all clients
                    self.socketio.emit('notification', {
                        'type': 'info',
                        'message': f'Scenario changed to: {scenario_id}',
                        'timestamp': time.time()
                    })
                else:
                    emit('error', {'message': f'Failed to start scenario: {scenario_id}'})
            else:
                # Just update the scenario for next start
                emit('notification', {
                    'type': 'info',
                    'message': f'Scenario set to: {scenario_id} (simulation not running)',
                    'timestamp': time.time()
                })
        
        except Exception as e:
            emit('error', {
                'message': f'Error changing scenario: {str(e)}'
            })
    
    def on_subscribe(self, data):
        """Handle subscription to events"""
        client_id = request.sid
        
        if client_id not in self.connected_clients:
            emit('error', {'message': 'Client not connected'})
            return
        
        event_type = data.get('event_type')
        
        if not event_type:
            emit('error', {'message': 'No event_type specified'})
            return
        
        # Add subscription
        if client_id in self.client_info:
            self.client_info[client_id]['subscriptions'].add(event_type)
        
        emit('subscription_update', {
            'event_type': event_type,
            'subscribed': True,
            'message': f'Subscribed to {event_type} events'
        })
    
    def on_unsubscribe(self, data):
        """Handle unsubscription from events"""
        client_id = request.sid
        
        if client_id not in self.connected_clients:
            emit('error', {'message': 'Client not connected'})
            return
        
        event_type = data.get('event_type')
        
        if not event_type:
            emit('error', {'message': 'No event_type specified'})
            return
        
        # Remove subscription
        if client_id in self.client_info and event_type in self.client_info[client_id]['subscriptions']:
            self.client_info[client_id]['subscriptions'].remove(event_type)
        
        emit('subscription_update', {
            'event_type': event_type,
            'subscribed': False,
            'message': f'Unsubscribed from {event_type} events'
        })
    
    def get_connected_clients_count(self) -> int:
        """Get number of connected clients"""
        return len(self.connected_clients)
    
    def broadcast(self, event: str, data: dict, room: str = None):
        """Broadcast event to all or specific room"""
        if room:
            self.socketio.emit(event, data, room=room)
        else:
            self.socketio.emit(event, data)


def register_socketio_handlers(socketio, simulator, simulation_stream):
    """Register WebSocket handlers"""
    manager = WebSocketManager(socketio, simulator, simulation_stream)
    return manager