"""
Scenario model
"""
from datetime import datetime
from .simulation import db

class Scenario(db.Model):
    """Traffic simulation scenario"""
    __tablename__ = 'scenarios'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    vehicle_count = db.Column(db.Integer, default=100)
    traffic_density = db.Column(db.String(20), default='medium')  # low, medium, high, very-high
    has_emergency_vehicles = db.Column(db.Boolean, default=False)
    duration = db.Column(db.Integer, default=3600)  # seconds
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'vehicleCount': self.vehicle_count,
            'trafficDensity': self.traffic_density,
            'hasEmergencyVehicles': self.has_emergency_vehicles,
            'duration': self.duration,
            'isActive': self.is_active,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_default_scenarios(cls):
        """Get default scenarios"""
        return [
            cls(
                id='default',
                name='Trafic Normal',
                description='Trafic urbain standard',
                vehicle_count=100,
                traffic_density='medium',
                has_emergency_vehicles=False,
                duration=3600
            ),
            cls(
                id='rush_hour',
                name='Heure de Pointe',
                description='Pic de trafic du matin',
                vehicle_count=250,
                traffic_density='very-high',
                has_emergency_vehicles=True,
                duration=7200
            ),
            cls(
                id='emergency_test',
                name='Test Urgence',
                description='Scénario avec véhicules prioritaires',
                vehicle_count=80,
                traffic_density='low',
                has_emergency_vehicles=True,
                duration=1800
            ),
            cls(
                id='weekend',
                name='Week-end Léger',
                description='Trafic réduit de week-end',
                vehicle_count=60,
                traffic_density='low',
                has_emergency_vehicles=False,
                duration=5400
            )
        ]