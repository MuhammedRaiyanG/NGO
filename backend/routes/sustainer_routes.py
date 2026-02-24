from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Sustainer, Admin

bp = Blueprint('sustainers', __name__, url_prefix='/api/sustainers')

@bp.route('/', methods=['POST'])
def register_sustainer():
    """Register as a monthly sustainer/donor"""
    data = request.get_json()
    
    required_fields = ['full_name', 'email', 'phone', 'monthly_amount', 'payment_method']
    if not data or not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    # Validate amount
    try:
        amount = float(data['monthly_amount'])
        if amount < 100:
            return {'error': 'Minimum monthly amount is ₹100'}, 400
    except (ValueError, TypeError):
        return {'error': 'Invalid amount'}, 400
    
    sustainer = Sustainer(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        monthly_amount=amount,
        payment_method=data['payment_method']
    )
    
    db.session.add(sustainer)
    db.session.commit()
    
    return {
        'message': 'Thank you for becoming a sustainer! We will contact you with payment details.',
        'sustainer': sustainer.to_dict()
    }, 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_sustainers():
    """Get all sustainers (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    sustainers = Sustainer.query.all()
    total_monthly = sum(s.monthly_amount for s in sustainers if s.status == 'active')
    
    return {
        'total': len(sustainers),
        'active': len([s for s in sustainers if s.status == 'active']),
        'total_monthly_mrr': total_monthly,
        'sustainers': [s.to_dict() for s in sustainers]
    }, 200

@bp.route('/<int:sustainer_id>', methods=['GET'])
@jwt_required()
def get_sustainer(sustainer_id):
    """Get specific sustainer details"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    sustainer = Sustainer.query.get(sustainer_id)
    
    if not sustainer:
        return {'error': 'Sustainer not found'}, 404
    
    return {'sustainer': sustainer.to_dict()}, 200

@bp.route('/<int:sustainer_id>', methods=['PUT'])
@jwt_required()
def update_sustainer_status(sustainer_id):
    """Update sustainer status (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    sustainer = Sustainer.query.get(sustainer_id)
    
    if not sustainer:
        return {'error': 'Sustainer not found'}, 404
    
    if 'status' in data:
        valid_statuses = ['active', 'paused', 'cancelled', 'pending']
        if data['status'] not in valid_statuses:
            return {'error': 'Invalid status'}, 400
        sustainer.status = data['status']
    
    if 'monthly_amount' in data:
        try:
            amount = float(data['monthly_amount'])
            if amount < 100:
                return {'error': 'Minimum monthly amount is ₹100'}, 400
            sustainer.monthly_amount = amount
        except (ValueError, TypeError):
            return {'error': 'Invalid amount'}, 400
    
    db.session.commit()
    
    return {
        'message': 'Sustainer updated',
        'sustainer': sustainer.to_dict()
    }, 200

@bp.route('/<int:sustainer_id>', methods=['DELETE'])
@jwt_required()
def delete_sustainer(sustainer_id):
    """Delete sustainer record (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    sustainer = Sustainer.query.get(sustainer_id)
    
    if not sustainer:
        return {'error': 'Sustainer not found'}, 404
    
    db.session.delete(sustainer)
    db.session.commit()
    
    return {'message': 'Sustainer deleted'}, 200

@bp.route('/count', methods=['GET'])
def get_sustainer_count():
    """Get public sustainer count and monthly revenue target"""
    active_sustainers = Sustainer.query.filter_by(status='active').all()
    total_count = Sustainer.query.count()
    total_monthly = sum(s.monthly_amount for s in active_sustainers)
    
    return {
        'total_sustainers': total_count,
        'active_sustainers': len(active_sustainers),
        'total_monthly_mrr': total_monthly
    }, 200
