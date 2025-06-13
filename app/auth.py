from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    from app.models import Customer
    from app import db
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required.'}), 400
    if Customer.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 400
    hashed_pw = generate_password_hash(password)
    customer = Customer(id=uuid.uuid4(), email=email, points=0)
    customer.password_hash = hashed_pw
    db.session.add(customer)
    db.session.commit()
    return jsonify({'message': 'Registration successful.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    from app.models import Customer
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required.'}), 400
    customer = Customer.query.filter_by(email=email).first()
    if not customer or not hasattr(customer, 'password_hash') or not check_password_hash(customer.password_hash, password):
        return jsonify({'error': 'Invalid credentials.'}), 401
    access_token = create_access_token(identity=str(customer.id))
    return jsonify({'access_token': access_token}), 200 