from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Admin, ImpactMetric, Volunteer, ContactMessage, Donation
import os
import json
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get admin dashboard statistics"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    volunteers_count = Volunteer.query.count()
    pending_volunteers = Volunteer.query.filter_by(status='pending').count()
    
    contacts_count = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(status='unread').count()
    
    donations_count = Donation.query.count()
    confirmed_donations = Donation.query.filter_by(status='confirmed').count()
    total_amount = sum(d.amount for d in Donation.query.filter_by(status='confirmed').all())
    
    return {
        'volunteers': {
            'total': volunteers_count,
            'pending': pending_volunteers
        },
        'contacts': {
            'total': contacts_count,
            'unread': unread_messages
        },
        'donations': {
            'total': donations_count,
            'confirmed': confirmed_donations,
            'total_amount': total_amount
        }
    }, 200

@bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    """Get all impact metrics"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    metrics = ImpactMetric.query.all()
    return {
        'metrics': [m.to_dict() for m in metrics]
    }, 200

@bp.route('/metrics/<metric_name>', methods=['PUT'])
@jwt_required()
def update_metric(metric_name):
    """Update an impact metric"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    if 'metric_value' not in data:
        return {'error': 'Missing metric_value'}, 400
    
    try:
        value = int(data['metric_value'])
    except ValueError:
        return {'error': 'metric_value must be an integer'}, 400
    
    metric = ImpactMetric.query.filter_by(metric_name=metric_name).first()
    
    if not metric:
        return {'error': 'Metric not found'}, 404
    
    metric.metric_value = value
    metric.updated_by = admin_id
    
    db.session.commit()
    
    return {
        'message': 'Metric updated successfully',
        'metric': metric.to_dict()
    }, 200

@bp.route('/metrics', methods=['POST'])
@jwt_required()
def create_metric():
    """Create a new impact metric"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    data = request.get_json()
    
    required_fields = ['metric_name', 'metric_value', 'metric_description']
    if not all(field in data for field in required_fields):
        return {'error': 'Missing required fields'}, 400
    
    if ImpactMetric.query.filter_by(metric_name=data['metric_name']).first():
        return {'error': 'Metric already exists'}, 409
    
    try:
        value = int(data['metric_value'])
    except ValueError:
        return {'error': 'metric_value must be an integer'}, 400
    
    metric = ImpactMetric(
        metric_name=data['metric_name'],
        metric_value=value,
        metric_description=data['metric_description'],
        updated_by=admin_id
    )
    
    db.session.add(metric)
    db.session.commit()
    
    return {
        'message': 'Metric created successfully',
        'metric': metric.to_dict()
    }, 201

@bp.route('/metrics/<metric_name>', methods=['DELETE'])
@jwt_required()
def delete_metric(metric_name):
    """Delete an impact metric"""
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    
    if not admin:
        return {'error': 'Unauthorized'}, 403
    
    metric = ImpactMetric.query.filter_by(metric_name=metric_name).first()
    
    if not metric:
        return {'error': 'Metric not found'}, 404
    
    db.session.delete(metric)
    db.session.commit()
    
    return {'message': 'Metric deleted'}, 200


# Team endpoints (public GET, admin CRUD)
def _team_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'team.json')

def _load_team():
    p = _team_path()
    if not os.path.exists(p):
        return []
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_team(data):
    p = _team_path()
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Upload team member photo (admin only)
@bp.route('/team/upload', methods=['POST'])
@jwt_required()
def upload_team_photo():
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    if not admin:
        return {'error': 'Unauthorized'}, 403

    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1]
    import uuid
    filename = f"{uuid.uuid4().hex}{ext}"

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, filename)
    file.save(save_path)

    # Return relative URL that the frontend can use
    url = f"/uploads/{filename}"
    return {'url': url}, 201


# Public team list
@bp.route('/team', methods=['GET'])
def public_team():
    team = _load_team()
    return {'team': team}, 200


# Admin: get team (protected)
@bp.route('/team/admin', methods=['GET'])
@jwt_required()
def get_team_admin():
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    if not admin:
        return {'error': 'Unauthorized'}, 403
    team = _load_team()
    return {'team': team}, 200


@bp.route('/team', methods=['POST'])
@jwt_required()
def add_team_member():
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    if not admin:
        return {'error': 'Unauthorized'}, 403
    data = request.get_json() or {}
    required = ['full_name', 'role', 'photo']
    if not all(k in data for k in required):
        return {'error': 'Missing required fields'}, 400
    team = _load_team()
    new_id = max([m.get('id', 0) for m in team] + [0]) + 1
    member = {'id': new_id, 'full_name': data['full_name'], 'role': data['role'], 'photo': data['photo']}
    team.append(member)
    _save_team(team)
    return {'message': 'Member added', 'member': member}, 201


@bp.route('/team/<int:member_id>', methods=['PUT'])
@jwt_required()
def update_team_member(member_id):
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    if not admin:
        return {'error': 'Unauthorized'}, 403
    data = request.get_json() or {}
    team = _load_team()
    member = next((m for m in team if m.get('id') == member_id), None)
    if not member:
        return {'error': 'Member not found'}, 404
    # allow updating fields
    for k in ('full_name', 'role', 'photo'):
        if k in data:
            member[k] = data[k]
    _save_team(team)
    return {'message': 'Member updated', 'member': member}, 200


@bp.route('/team/<int:member_id>', methods=['DELETE'])
@jwt_required()
def delete_team_member(member_id):
    admin_id = int(get_jwt_identity())
    admin = Admin.query.get(admin_id)
    if not admin:
        return {'error': 'Unauthorized'}, 403
    team = _load_team()
    new_team = [m for m in team if m.get('id') != member_id]
    if len(new_team) == len(team):
        return {'error': 'Member not found'}, 404
    _save_team(new_team)
    return {'message': 'Member deleted'}, 200
