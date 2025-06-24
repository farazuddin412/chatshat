from flask import Flask,request, jsonify,render_template,url_for,redirect
from app import app,socketio
from models.UserModel import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import db
from flask_socketio import send
import random
from models.RoomsModel import Room
from models.Messages import Message as MessageModel
from flask_socketio import send, emit, join_room




jwt = JWTManager(app)

def generate_otp():
    otp = random.randint(100000,999999)

@app.route('/')
def home():
    print(request)
    return render_template('message.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    send("Welcome!", broadcast=True)
        


@socketio.on("message")  # Handle incoming messages
def handle_message(data):
    print(data,'data')
    room_id = data.get("room_id")
    sender_id = data.get("sender_id")
    message_text = data.get("message")

    print(f"Message received: {message_text}")
    # send(data, broadcast=True)
     # Validation check
    if not room_id or not sender_id or not message_text:
        return jsonify({"error": "Missing fields"}), 400
    
    message = MessageModel(
        room_id=room_id,
        sender_id=sender_id,
        message=message_text
    )
    db.session.add(message)
    db.session.commit()

     # Broadcast message to the room
    emit(
        "message",
        {
            "id": message.id,
            "room_id": message.room_id,
            "sender_id": message.sender_id,
            "message": message.message,
            "timestamp": str(message.timestamp)
        },
        room=room_id  # Only send message to users in this room
    )


@app.route('/message/<room_id>',methods=["GET"])
def get_message(room_id):
    print(room_id,'room')
    if not room_id:
         return jsonify({"error": "room_id is required"}), 400
    
    messages= MessageModel.query.filter_by(room_id=room_id).order_by('timestamp').all()

    print(messages,'messages')
    result = [
        
        {
        'id' : msg.id,
        'room_id' : msg.room_id,
        'sender_id' : msg.sender_id,
        'message' : msg.message,
        'timestamp' : msg.timestamp
        }
        for msg in messages
    ]

    print(result,'result')
    return jsonify({'messages':result,'type':"messages"})


@app.route('/register',methods=['POST',"GET"])
def register():
    if request.method=="POST":
        print("JSON Data:", request)
        data=request.json
        hashed_password=generate_password_hash(data['password'],method='pbkdf2:sha256')
        new_user = User(email=data['email'],name=data['name'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!","status":"ok","success":True,"type":"user"})
    else:
        return render_template('register.html')

@app.route('/login',methods=['POST'])
def login():
    if request.method=="POST":
        data = request.json
        print(data)
        user = User.query.filter_by(email=data["email"]).first()  # Equivalent to WHERE name='Alice'
        print(repr(user))
        if user and check_password_hash(user.password, data["password"]):
            
            access_token = create_access_token(identity=user.id,
            additional_claims={"name": user.name,"email": user.email})
            return jsonify({
            "token": access_token,
            "message": "Login successful!",
            "type":"user"
            })
        else:
            return jsonify({"error": "Invalid email or password"}), 401
        


# join room for chat
@app.route('/join-room',methods=["POST"])
def join():
    data=request.json
    print(data)
    room_type=data['room_type']


    if room_type=='one-on-one':
        room = Room.query.filter_by(room_name=data['room_name']).first()
        if not room:
            room=Room(users=data['users'],room_type=room_type,room_name=data['room_name'])
            db.session.add(room)
            db.session.commit()
            return jsonify({"room_name":room.room_name,"room_id":room.id,"type":"room"})
        else:
            return jsonify({"room_name":room.room_name,"room_id":room.id,"type":"room"})
    else:
        pass


@socketio.on("join")
def on_join(data):
    room_id = data.get("room_id")
    join_room(room_id)
    print(f"User joined room {room_id}")



        
@app.route('/users',methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(users_list)

    
    


    

    