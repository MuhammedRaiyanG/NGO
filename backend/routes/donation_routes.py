from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Donation, Admin

bp = Blueprint('donations', __name__, url_prefix='/api/donations')

@bp.route('/', methods=['POST'])
def create_donation():
    """Record a donation"""
    data = request.get_json()
    
    required_fields = ['donor_name', 'donor_email', 'amount', 'donation_type']
    if not data or not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return {'error': 'Amount must be greater than 0'}, 400
    except ValueError:
        return {'error': 'Invalid amount'}, 400
    
    donation = Donation(
        donor_name=data['donor_name'],
        donor_email=data['donor_email'],
        amount=amount,
        donation_type=data['donation_type'],
        transaction_id=data.get('transaction_id'),
        status=data.get('status', 'pending')
    )
    
    db.session.add(donation)
    db.session.commit()
    
    return {
        'message': 'Donation recorded successfully',
        'donation': donation.to_dict()
    }, 201

@bp.route('/', methods=['GET'])
@jwt_required()
def get_donations():
    """Get all donations (admin only)"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    donations = Donation.query.all()
    confirmed_donations = [d for d in donations if d.status == 'confirmed']
    total_amount = sum(d.amount for d in confirmed_donations)
    
    return {
        'total_donations': len(donations),
        'confirmed_donations': len(confirmed_donations),
        'total_amount': total_amount,
        'donations': [d.to_dict() for d in donations]
    }, 200

@bp.route('/<int:donation_id>', methods=['GET'])
@jwt_required()
def get_donation(donation_id):
    """Get specific donation"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    donation = Donation.query.get(donation_id)
    if not donation:
        return {'error': 'Donation not found'}, 404
    
    return {'donation': donation.to_dict()}, 200

@bp.route('/<int:donation_id>', methods=['PUT'])
@jwt_required()
def update_donation(donation_id):
    """Update donation status"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    donation = Donation.query.get(donation_id)
    if not donation:
        return {'error': 'Donation not found'}, 404
    
    data = request.get_json()
    
    if 'status' in data:
        if data['status'] not in ['pending', 'confirmed', 'failed']:
            return {'error': 'Invalid status'}, 400
        donation.status = data['status']
    
    db.session.commit()
    
    return {'message': 'Donation updated', 'donation': donation.to_dict()}, 200

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_donation_stats():
    """Get donation statistics"""
    admin_id = get_jwt_identity()
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    donations = Donation.query.all()
    confirmed = [d for d in donations if d.status == 'confirmed']
    
    stats = {
        'total_amount': sum(d.amount for d in confirmed),
        'total_donors': len(set(d.donor_email for d in confirmed)),
        'donation_count': len(confirmed),
        'by_type': {}
    }
    
    for donation_type in ['bank', 'upi', 'monthly']:
        type_donations = [d for d in confirmed if d.donation_type == donation_type]
        stats['by_type'][donation_type] = {
            'count': len(type_donations),
            'amount': sum(d.amount for d in type_donations)
        }
    
    return stats, 200
