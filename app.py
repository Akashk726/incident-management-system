# app.py
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import os
from datetime import datetime
import jwt
from functools import wraps
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incidents.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'akash98854@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'ypyv mkhf apuc pmqr'     # Replace with your app password
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, technician, user

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')
    priority = db.Column(db.String(20), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
        session['token'] = token
        return jsonify({'token': token, 'role': user.role})
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/incidents', methods=['POST'])
@token_required
def create_incident(current_user):
    data = request.get_json()
    incident = Incident(
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        created_by=current_user.id
    )
    db.session.add(incident)
    db.session.commit()
    
    # Send email notification
    msg = Message('New Incident Created', 
                 sender=app.config['MAIL_USERNAME'],
                 recipients=['admin@example.com'])
    msg.body = f"New incident: {data['title']}\nDescription: {data['description']}"
    mail.send(msg)
    
    return jsonify({'message': 'Incident created successfully!'})

@app.route('/incidents', methods=['GET'])
@token_required
def get_incidents(current_user):
    incidents = Incident.query.all()
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'description': i.description,
        'status': i.status,
        'priority': i.priority,
        'created_at': i.created_at
    } for i in incidents])

@app.route('/incidents/<int:id>', methods=['PUT'])
@token_required
def update_incident(current_user, id):
    if current_user.role != 'admin' and current_user.role != 'technician':
        return jsonify({'message': 'Unauthorized!'}), 403
    
    data = request.get_json()
    incident = Incident.query.get_or_404(id)
    incident.status = data.get('status', incident.status)
    incident.assigned_to = data.get('assigned_to', incident.assigned_to)
    incident.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Incident updated successfully!'})

@app.route('/dashboard')
@token_required
def dashboard(current_user):
    incidents = Incident.query.filter_by(created_by=current_user.id).all()
    return render_template('dashboard.html', incidents=incidents, role=current_user.role)

# Database initialization
def init_db():
    with app.app_context():
        db.create_all()
        # Create sample users
        if not User.query.first():
            admin = User(username='admin', 
                        password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                        role='admin')
            tech = User(username='tech', 
                       password=bcrypt.generate_password_hash('tech123').decode('utf-8'),
                       role='technician')
            user = User(username='user', 
                       password=bcrypt.generate_password_hash('user123').decode('utf-8'),
                       role='user')
            db.session.add_all([admin, tech, user])
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
