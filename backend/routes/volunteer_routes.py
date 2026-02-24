from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Volunteer, Admin

bp = Blueprint('volunteers', __name__, url_prefix='/api/volunteers')

@bp.route('/', methods=['POST'])
def register_volunteer():
    """Register as a volunteer"""
    data = request.get_json()
    
    required_fields = ['full_name', 'email', 'phone', 'interested_area']
    if not data or not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    volunteer = Volunteer(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        interested_area=data['interested_area']
    )
    
    db.session.add(volunteer)
    db.session.commit()
    
    return {
        'message': 'Volunteer registration successful',
        'volunteer': volunteer.to_dict()
    }, 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_volunteers():
    """Get all volunteer registrations (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    volunteers = Volunteer.query.all()
    return {
        'total': len(volunteers),
        'volunteers': [v.to_dict() for v in volunteers]
    }, 200

@bp.route('/<int:volunteer_id>', methods=['GET'])
@jwt_required()
def get_volunteer(volunteer_id):
    """Get specific volunteer details"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {'error': 'Volunteer not found'}, 404
    
    return {'volunteer': volunteer.to_dict()}, 200

@bp.route('/<int:volunteer_id>', methods=['PUT'])
@jwt_required()
def update_volunteer(volunteer_id):
    """Update volunteer status (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {'error': 'Volunteer not found'}, 404
    
    data = request.get_json()
    
    if 'status' in data:
        if data['status'] not in ['pending', 'approved', 'rejected']:
            return {'error': 'Invalid status'}, 400
        volunteer.status = data['status']
    
    db.session.commit()
    
    return {'message': 'Volunteer updated', 'volunteer': volunteer.to_dict()}, 200

@bp.route('/<int:volunteer_id>', methods=['DELETE'])
@jwt_required()
def delete_volunteer(volunteer_id):
    """Delete volunteer record"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {'error': 'Volunteer not found'}, 404
    
    db.session.delete(volunteer)
    db.session.commit()
    
    return {'message': 'Volunteer deleted'}, 200
