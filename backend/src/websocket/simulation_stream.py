import threading
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimulationStream:
    """Gère l'envoi périodique des données de simulation via WebSocket"""
    
    def __init__(self, socketio, simulator):
        """
        Initialise le flux de simulation
        
        Args:
            socketio: Instance de SocketIO Flask
            simulator: Instance du simulateur (MockSimulator)
        """
        self.socketio = socketio
        self.simulator = simulator
        self.stream_thread = None
        self.streaming = False
        self.update_interval = 0.1  # 100ms
        self.metrics_interval = 0.5  # 500ms
        self.last_metrics_time = time.time()
        
    def start_streaming(self) -> bool:
        """
        Démarrer l'envoi périodique des données
        
        Returns:
            bool: True si démarré avec succès, False si déjà en cours
        """
        if self.streaming:
            logger.warning("Streaming déjà en cours")
            return False
            
        logger.info("Démarrage du flux de simulation WebSocket")
        self.streaming = True
        self.last_metrics_time = time.time()
        
        # Créer et démarrer le thread
        self.stream_thread = threading.Thread(
            target=self._stream_loop,
            daemon=True,
            name="SimulationStream"
        )
        self.stream_thread.start()
        
        return True
        
    def stop_streaming(self) -> bool:
        """
        Arrêter l'envoi des données
        
        Returns:
            bool: True si arrêté avec succès
        """
        if not self.streaming:
            return True
            
        logger.info("Arrêt du flux de simulation WebSocket")
        self.streaming = False
        
        # Attendre que le thread se termine proprement
        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=2.0)
            if self.stream_thread.is_alive():
                logger.warning("Thread de streaming toujours actif après timeout")
                
        self.stream_thread = None
        return True
        
    def _stream_loop(self):
        """
        Boucle principale d'envoi des données
        Tourne dans un thread séparé
        """
        logger.info("Boucle de streaming démarrée")
        
        try:
            while self.streaming:
                loop_start_time = time.time()
                
                try:
                    # Vérifier si la simulation est active
                    if self.simulator.is_running and not self.simulator.is_paused:
                        # Mettre à jour la simulation
                        self.simulator.update_simulation(self.update_interval)
                        
                        # Récupérer les données actuelles
                        data = self.simulator.get_simulation_data()
                        
                        # Envoyer les mises à jour complètes
                        self._emit_simulation_update(data)
                        
                        # Envoyer les métriques moins fréquemment
                        current_time = time.time()
                        if current_time - self.last_metrics_time >= self.metrics_interval:
                            self._emit_metrics_update(data['metrics'])
                            self.last_metrics_time = current_time
                            
                    elif self.simulator.is_paused:
                        # Simulation en pause - envoyer uniquement l'état
                        self._emit_pause_status()
                        
                except Exception as e:
                    logger.error(f"Erreur dans la boucle de streaming: {e}", exc_info=True)
                    self._emit_error(str(e))
                    
                # Contrôler la fréquence d'envoi
                loop_duration = time.time() - loop_start_time
                sleep_time = max(0, self.update_interval - loop_duration)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                elif loop_duration > self.update_interval * 1.5:
                    logger.warning(f"Boucle de streaming trop lente: {loop_duration:.3f}s")
                    
        except Exception as e:
            logger.error(f"Boucle de streaming terminée avec erreur: {e}", exc_info=True)
        finally:
            logger.info("Boucle de streaming terminée")
            self.streaming = False
            
    def _emit_simulation_update(self, data: Dict[str, Any]):
        """
        Émettre une mise à jour complète de simulation
        
        Args:
            data: Données de simulation
        """
        try:
            self.socketio.emit('simulation_update', {
                'vehicles': data.get('vehicles', []),
                'traffic_lights': data.get('traffic_lights', []),
                'timestamp': data.get('timestamp'),
                'simulation_time': data.get('simulation_time', 0),
                'update_id': int(time.time() * 1000)  # ID unique pour le suivi
            })
        except Exception as e:
            logger.error(f"Erreur lors de l'émission simulation_update: {e}")
            
    def _emit_metrics_update(self, metrics: Dict[str, Any]):
        """
        Émettre une mise à jour des métriques
        
        Args:
            metrics: Métriques de simulation
        """
        try:
            self.socketio.emit('metrics_update', {
                'metrics': metrics,
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Erreur lors de l'émission metrics_update: {e}")
            
    def _emit_pause_status(self):
        """Émettre l'état de pause"""
        try:
            self.socketio.emit('simulation_status', {
                'status': 'paused',
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Erreur lors de l'émission pause status: {e}")
            
    def _emit_error(self, error_message: str):
        """
        Émettre une erreur
        
        Args:
            error_message: Message d'erreur
        """
        try:
            self.socketio.emit('error', {
                'message': error_message,
                'timestamp': time.time(),
                'type': 'stream_error'
            })
        except Exception as e:
            logger.error(f"Erreur lors de l'émission d'erreur: {e}")
            
    def update_settings(self, update_interval: float = None, metrics_interval: float = None):
        """
        Mettre à jour les paramètres du streaming
        
        Args:
            update_interval: Nouvel intervalle de mise à jour (secondes)
            metrics_interval: Nouvel intervalle pour les métriques (secondes)
        """
        if update_interval is not None:
            self.update_interval = max(0.01, min(1.0, update_interval))  # Limite 10ms-1s
            logger.info(f"Intervalle de mise à jour changé à {self.update_interval}s")
            
        if metrics_interval is not None:
            self.metrics_interval = max(0.1, min(5.0, metrics_interval))  # Limite 100ms-5s
            logger.info(f"Intervalle des métriques changé à {self.metrics_interval}s")
            
    def get_status(self) -> Dict[str, Any]:
        """
        Récupérer le statut actuel du streaming
        
        Returns:
            Dict avec les informations de statut
        """
        return {
            'streaming': self.streaming,
            'update_interval': self.update_interval,
            'metrics_interval': self.metrics_interval,
            'thread_alive': self.stream_thread.is_alive() if self.stream_thread else False,
            'simulator_running': self.simulator.is_running,
            'simulator_paused': self.simulator.is_paused
        }