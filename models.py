from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Measurement(db.Model):
    __tablename__ = "measurements"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    hostname = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    memory_usage = db.Column(db.Float, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
        }
