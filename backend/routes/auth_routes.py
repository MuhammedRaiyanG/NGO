from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Admin

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """Admin login"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return {'error': 'Missing username or password'}, 400
    
    admin = Admin.query.filter_by(username=data['username']).first()
    
    if not admin or not admin.check_password(data['password']):
        return {'error': 'Invalid credentials'}, 401
    
    access_token = create_access_token(identity=str(admin.id))
    return {
        'access_token': access_token,
        'admin': admin.to_dict()
    }, 200

@bp.route('/register', methods=['POST'])
def register():
    """Admin registration (protected - only existing admins can register new ones)"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return {'error': 'Missing required fields'}, 400
    
    if Admin.query.filter_by(username=data['username']).first():
        return {'error': 'Username already exists'}, 409
    
    if Admin.query.filter_by(email=data['email']).first():
        return {'error': 'Email already exists'}, 409
    
    admin = Admin(username=data['username'], email=data['email'])
    admin.set_password(data['password'])
    
    db.session.add(admin)
    db.session.commit()
    
    return {'message': 'Admin registered successfully', 'admin': admin.to_dict()}, 201

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current admin profile"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Admin not found'}, 404
    
    return {'admin': admin.to_dict()}, 200
