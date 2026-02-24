from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    """Admin user model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Volunteer(db.Model):
    """Volunteer registration model"""
    __tablename__ = 'volunteers'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    interested_area = db.Column(db.String(100), nullable=False)  # women_safety, recovery, blood_donation
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'interested_area': self.interested_area,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class ContactMessage(db.Model):
    """Contact form submissions"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # unread, read, replied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Donation(db.Model):
    """Donation records"""
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(120), nullable=False)
    donor_email = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_type = db.Column(db.String(50), nullable=False)  # bank, upi, monthly
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'donor_name': self.donor_name,
            'donor_email': self.donor_email,
            'amount': self.amount,
            'donation_type': self.donation_type,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class ImpactMetric(db.Model):
    """Impact metrics (editable by admins)"""
    __tablename__ = 'impact_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), unique=True, nullable=False)
    metric_value = db.Column(db.Integer, nullable=False)
    metric_description = db.Column(db.String(200), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_description': self.metric_description,
            'updated_at': self.updated_at.isoformat()
        }
class Sustainer(db.Model):
    """Monthly sustainer/recurring donor model"""
    __tablename__ = 'sustainers'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    monthly_amount = db.Column(db.Float, nullable=False)  # ₹500, ₹1000, ₹5000, etc
    payment_method = db.Column(db.String(50), nullable=False)  # upi, bank, card
    status = db.Column(db.String(20), default='pending')  # pending, active, paused, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'monthly_amount': self.monthly_amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }