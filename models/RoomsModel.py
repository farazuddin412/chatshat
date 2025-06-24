from flask import Flask
from app import db
from models.getDefaultId import generate_custom_id

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.String(20), primary_key=True, default=lambda: generate_custom_id("Room"))
    room_name=db.Column(db.String(100), nullable=False,unique=True)
    users = db.Column(db.JSON, nullable=False)
    room_type = db.Column(db.Enum('one-on-one', 'group'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


    def to_dict(self):
        return {"id": self.id, "users": self.users,"type":"User","type":self.type,"created_at":self.created_at}
    

