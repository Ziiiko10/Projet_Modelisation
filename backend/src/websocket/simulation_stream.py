"""
Real-time simulation data streaming
"""
import threading
import time
import json
from datetime import datetime
from typing import Dict, Any

class SimulationStream:
    """
    Manages real-time streaming of simulation data via WebSocket
    """
    
    def __init__(self, socketio, simulator):
        self.socketio = socketio
        self.simulator = simulator
        self.stream_thread = None
        self.streaming = False
        self.update_interval = 0.1  # 100ms
        self.last_metrics_update = 0
        self.metrics_interval = 2.0  # Update metrics every 2 seconds
        self.last_vehicle_update = 0
        self.vehicle_interval = 0.5  # Update vehicles every 500ms
        self.clients = {}  # Track connected clients
        
        print("📡 Simulation stream initialized")
    
    def start_streaming(self):
        """Start streaming simulation data"""
        if self.streaming:
            print("⚠️ Streaming already active")
            return
        
        self.streaming = True
        self.stream_thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.stream_thread.start()
        
        print("🚀 Simulation stream started")
    
    def stop_streaming(self):
        """Stop streaming simulation data"""
        self.streaming = False
        
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=2.0)
        
        print("⏹️ Simulation stream stopped")
    
    def _stream_loop(self):
        """Main streaming loop"""
        print("🔄 Starting simulation stream loop")
        
        while self.streaming:
            try:
                current_time = time.time()
                
                # Check if simulation is running and not paused
                if self.simulator.is_running and not self.simulator.is_paused:
                    # Update simulation
                    self.simulator.update_simulation(self.update_interval)
                    
                    # Get simulation data
                    simulation_data = self.simulator.get_simulation_data()
                    
                    # Send full simulation update (less frequent)
                    if int(current_time * 10) % 2 == 0:  # Every 200ms
                        self.socketio.emit('simulation_update', simulation_data)
                    
                    # Send vehicle updates (more frequent)
                    if current_time - self.last_vehicle_update >= self.vehicle_interval:
                        vehicle_data = {
                            'vehicles': simulation_data['vehicles'],
                            'count': len(simulation_data['vehicles']),
                            'timestamp': datetime.utcnow().isoformat()
                        }
                        self.socketio.emit('vehicle_update', vehicle_data)
                        self.last_vehicle_update = current_time
                    
                    # Send traffic light updates
                    traffic_light_data = {
                        'traffic_lights': simulation_data['traffic_lights'],
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    self.socketio.emit('traffic_light_update', traffic_light_data)
                    
                    # Send metrics updates (less frequent)
                    if current_time - self.last_metrics_update >= self.metrics_interval:
                        metrics_data = {
                            'metrics': simulation_data['metrics'],
                            'timestamp': datetime.utcnow().isoformat()
                        }
                        self.socketio.emit('metrics_update', metrics_data)
                        self.last_metrics_update = current_time
                    
                    # Send simulation status periodically
                    if int(current_time) % 5 == 0:  # Every 5 seconds
                        status_data = {
                            'status': 'running',
                            'is_paused': False,
                            'current_scenario': self.simulator.current_scenario,
                            'simulation_time': self.simulator.simulation_time,
                            'vehicle_count': len(self.simulator.vehicles),
                            'timestamp': datetime.utcnow().isoformat()
                        }
                        self.socketio.emit('simulation_status', status_data)
                
                else:
                    # Simulation is stopped or paused
                    if int(current_time) % 10 == 0:  # Every 10 seconds
                        status = 'paused' if self.simulator.is_paused else 'stopped'
                        status_data = {
                            'status': status,
                            'is_paused': self.simulator.is_paused,
                            'current_scenario': self.simulator.current_scenario,
                            'simulation_time': self.simulator.simulation_time,
                            'timestamp': datetime.utcnow().isoformat()
                        }
                        self.socketio.emit('simulation_status', status_data)
                
                # Small sleep to prevent CPU overload
                time.sleep(self.update_interval)
            
            except Exception as e:
                print(f"❌ Error in stream loop: {e}")
                # Send error to clients
                self.socketio.emit('error', {
                    'message': f'Stream error: {str(e)}',
                    'timestamp': datetime.utcnow().isoformat()
                })
                # Small delay before retry
                time.sleep(1.0)
    
    def send_immediate_update(self):
        """Send immediate update to all clients"""
        if self.simulator.is_running:
            simulation_data = self.simulator.get_simulation_data()
            
            # Send all updates immediately
            self.socketio.emit('simulation_update', simulation_data)
            
            # Send individual component updates
            self.socketio.emit('vehicle_update', {
                'vehicles': simulation_data['vehicles'],
                'count': len(simulation_data['vehicles']),
                'timestamp': datetime.utcnow().isoformat()
            })
            
            self.socketio.emit('traffic_light_update', {
                'traffic_lights': simulation_data['traffic_lights'],
                'timestamp': datetime.utcnow().isoformat()
            })
            
            self.socketio.emit('metrics_update', {
                'metrics': simulation_data['metrics'],
                'timestamp': datetime.utcnow().isoformat()
            })
            
            print("📤 Sent immediate update to all clients")
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Get streaming status"""
        return {
            'streaming': self.streaming,
            'update_interval': self.update_interval,
            'connected_clients': len(self.clients),
            'simulation_running': self.simulator.is_running,
            'simulation_paused': self.simulator.is_paused,
            'vehicle_count': len(self.simulator.vehicles),
            'last_update': datetime.utcnow().isoformat()
        }
    
    def register_client(self, client_id: str, client_info: Dict = None):
        """Register a new client"""
        self.clients[client_id] = {
            'registered_at': time.time(),
            'last_activity': time.time(),
            'info': client_info or {}
        }
        
        print(f"👤 Client registered: {client_id}")
    
    def unregister_client(self, client_id: str):
        """Unregister a client"""
        if client_id in self.clients:
            del self.clients[client_id]
            print(f"👋 Client unregistered: {client_id}")
    
    def update_client_activity(self, client_id: str):
        """Update client activity timestamp"""
        if client_id in self.clients:
            self.clients[client_id]['last_activity'] = time.time()
    
    def send_to_client(self, client_id: str, event: str, data: Dict):
        """Send data to specific client"""
        if client_id in self.clients:
            self.socketio.emit(event, data, room=client_id)
            self.update_client_activity(client_id)
    
    def broadcast(self, event: str, data: Dict, exclude_client: str = None):
        """Broadcast to all clients except specified one"""
        self.socketio.emit(event, data, skip_sid=exclude_client)