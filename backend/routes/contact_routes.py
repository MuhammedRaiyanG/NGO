from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ContactMessage, Admin

bp = Blueprint('contacts', __name__, url_prefix='/api/contacts')

@bp.route('/', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    data = request.get_json()
    
    required_fields = ['name', 'email', 'message']
    if not data or not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    contact = ContactMessage(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return {
        'message': 'Contact message received',
        'contact': contact.to_dict()
    }, 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_contacts():
    """Get all contact messages (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    contacts = ContactMessage.query.all()
    return {
        'total': len(contacts),
        'unread': len([c for c in contacts if c.status == 'unread']),
        'contacts': [c.to_dict() for c in contacts]
    }, 200

@bp.route('/<int:contact_id>', methods=['GET'])
@jwt_required()
def get_contact(contact_id):
    """Get specific contact message"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    contact = ContactMessage.query.get(contact_id)
    if not contact:
        return {'error': 'Contact message not found'}, 404
    
    return {'contact': contact.to_dict()}, 200

@bp.route('/<int:contact_id>', methods=['PUT'])
@jwt_required()
def update_contact(contact_id):
    """Update contact message status"""
    admin_id = get_jwt_identity()
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    contact = ContactMessage.query.get(contact_id)
    if not contact:
        return {'error': 'Contact message not found'}, 404
    
    data = request.get_json()
    
    if 'status' in data:
        if data['status'] not in ['unread', 'read', 'replied']:
            return {'error': 'Invalid status'}, 400
        contact.status = data['status']
    
    db.session.commit()
    
    return {'message': 'Contact updated', 'contact': contact.to_dict()}, 200

@bp.route('/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    """Delete contact message"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    contact = ContactMessage.query.get(contact_id)
    if not contact:
        return {'error': 'Contact message not found'}, 404
    
    db.session.delete(contact)
    db.session.commit()
    
    return {'message': 'Contact deleted'}, 200
