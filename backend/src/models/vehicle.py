"""
Vehicle model
"""
from datetime import datetime
from .simulation import db

class Vehicle(db.Model):
    """Vehicle in simulation"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.String(50), primary_key=True)
    vehicle_type = db.Column(db.String(20), default='passenger')  # passenger, emergency, bus, truck
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, default=0.0)  # km/h
    lane = db.Column(db.String(50))
    route = db.Column(db.Text)  # JSON string of route
    color = db.Column(db.String(10))
    heading = db.Column(db.Float, default=0.0)  # degrees
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        import json
        return {
            'id': self.id,
            'type': self.vehicle_type,
            'position': {'lat': self.lat, 'lng': self.lng},
            'speed': self.speed,
            'lane': self.lane,
            'route': json.loads(self.route) if self.route else [],
            'color': self.color,
            'heading': self.heading,
            'isActive': self.is_active
        }


class VehicleHistory(db.Model):
    """Historical vehicle data"""
    __tablename__ = 'vehicle_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'vehicleId': self.vehicle_id,
            'position': {'lat': self.lat, 'lng': self.lng},
            'speed': self.speed,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }