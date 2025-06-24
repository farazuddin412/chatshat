from flask import Flask
from app import db
from models.getDefaultId import generate_custom_id

class User(db.Model):
    __tablename__ = 'users' 
    id=db.Column(db.String(20),primary_key=True,default=lambda: generate_custom_id("User"))
    email=db.Column(db.String(100),nullable=False,unique=True)
    name=db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name,"type":"User"}
    

 