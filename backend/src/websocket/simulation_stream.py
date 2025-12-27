import threading
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimulationStream:
    """Gère l'envoi périodique des données via WebSocket"""
    
    def __init__(self, socketio, simulator):
        self.socketio = socketio
        self.simulator = simulator
        self.stream_thread = None
        self.streaming = False
        self.update_interval = 0.1  # 100ms
        self.metrics_interval = 0.5  # 500ms
        self.last_metrics_time = time.time()
        
    def start_streaming(self) -> bool:
        """Démarrer le streaming"""
        if self.streaming:
            logger.warning("Streaming déjà en cours")
            return False
            
        logger.info("Démarrage du flux WebSocket")
        self.streaming = True
        self.last_metrics_time = time.time()
        
        self.stream_thread = threading.Thread(
            target=self._stream_loop,
            daemon=True,
            name="SimulationStream"
        )
        self.stream_thread.start()
        
        return True
        
    def stop_streaming(self) -> bool:
        """Arrêter le streaming"""
        if not self.streaming:
            return True
            
        logger.info("Arrêt du flux WebSocket")
        self.streaming = False
        
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=2.0)
            if self.stream_thread.is_alive():
                logger.warning("Thread toujours actif après timeout")
                
        self.stream_thread = None
        return True
        
    def _stream_loop(self):
        """Boucle principale de streaming"""
        logger.info("Boucle de streaming démarrée")
        
        try:
            while self.streaming:
                loop_start_time = time.time()
                
                try:
                    if self.simulator.is_running and not self.simulator.is_paused:
                        self.simulator.update_simulation(self.update_interval)
                        data = self.simulator.get_simulation_data()
                        
                        # Envoyer les mises à jour
                        self._emit_simulation_update(data)
                        
                        # Envoyer métriques moins fréquemment
                        current_time = time.time()
                        if current_time - self.last_metrics_time >= self.metrics_interval:
                            self._emit_metrics_update(data['metrics'])
                            self.last_metrics_time = current_time
                            
                    elif self.simulator.is_paused:
                        self._emit_pause_status()
                        
                except Exception as e:
                    logger.error(f"Erreur dans boucle streaming: {e}", exc_info=True)
                    self._emit_error(str(e))
                    
                loop_duration = time.time() - loop_start_time
                sleep_time = max(0, self.update_interval - loop_duration)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                elif loop_duration > self.update_interval * 1.5:
                    logger.warning(f"Boucle trop lente: {loop_duration:.3f}s")
                    
        except Exception as e:
            logger.error(f"Boucle terminée avec erreur: {e}", exc_info=True)
        finally:
            logger.info("Boucle de streaming terminée")
            self.streaming = False
            
    def _emit_simulation_update(self, data: Dict[str, Any]):
        """Émettre une mise à jour de simulation"""
        try:
            self.socketio.emit('simulation_update', {
                'vehicles': data.get('vehicles', []),
                'traffic_lights': data.get('traffic_lights', []),
                'timestamp': data.get('timestamp'),
                'simulation_time': data.get('simulation_time', 0),
                'update_id': int(time.time() * 1000)
            })
        except Exception as e:
            logger.error(f"Erreur emission simulation_update: {e}")
            
    def _emit_metrics_update(self, metrics: Dict[str, Any]):
        """Émettre une mise à jour des métriques"""
        try:
            self.socketio.emit('metrics_update', {
                'metrics': metrics,
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Erreur emission metrics_update: {e}")
            
    def _emit_pause_status(self):
        """Émettre l'état de pause"""
        try:
            self.socketio.emit('simulation_status', {
                'status': 'paused',
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Erreur emission pause status: {e}")
            
    def _emit_error(self, error_message: str):
        """Émettre une erreur"""
        try:
            self.socketio.emit('error', {
                'message': error_message,
                'timestamp': time.time(),
                'type': 'stream_error'
            })
        except Exception as e:
            logger.error(f"Erreur emission erreur: {e}")