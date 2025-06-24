from flask import Flask
from app import db
from models.getDefaultId import generate_custom_id

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.String(20), primary_key=True, default=lambda: generate_custom_id("Message"))
    room_id = db.Column(db.String(20), db.ForeignKey("rooms.id"), nullable=False)
    sender_id = db.Column(db.String(20), db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def to_dict(self):
        """Convert message to dictionary format for easy JSON response."""
        return {
            "id": self.id,
            "room_id": self.room_id,
            "sender_id": self.sender_id,
            "message": self.message,
            "timestamp": self.timestamp
        }