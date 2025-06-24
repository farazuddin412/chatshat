from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import secrets
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_mail import Mail, Message
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

secret_key=secrets.token_hex(32)

app.secret_key=secret_key
app.config["JWT_SECRET_KEY"] = secret_key 

# MySQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/chatshat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
socketio = SocketIO(app,cors_allowed_origins='*')


# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your SMTP server
app.config['MAIL_PORT'] = 465  # Port for SSL
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'faraz.uddin.412@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'ifte romk blne nkpv'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'chatshat@gmail.com'

# Initialize the Mail extension
mail = Mail(app)




import route
from models import UserModel


with app.app_context():
        db.create_all()
        


# print(db,'db class')






