"""
Setup script to initialize the database with sample data
Run this after installing dependencies to populate the database
"""

import os
import sys
from app import create_app
from models import db, Admin, ImpactMetric, Volunteer, ContactMessage, Donation

def setup_database():
    """Initialize database with sample data"""
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Create default admin if it doesn't exist
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@hope.ngo')
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Default admin created (username: admin, password: admin123)")
            print("  WARNING: Change this password in production!")
        
        # Create default impact metrics
        default_metrics = [
            ('women_safety_centers', 18, 'women safety centers'),
            ('rehab_success_stories', 1450, 'rehab success stories'),
            ('blood_units_yearly', 4200, 'blood units/year'),
            ('legal_aid_cases', 312, 'legal aid cases'),
        ]
        
        for metric_name, value, description in default_metrics:
            if not ImpactMetric.query.filter_by(metric_name=metric_name).first():
                metric = ImpactMetric(
                    metric_name=metric_name,
                    metric_value=value,
                    metric_description=description
                )
                db.session.add(metric)
        
        print("✓ Impact metrics initialized")
        
        db.session.commit()
        print("\n✓ Database setup complete!")
        print("\nYou can now run: python app.py")

if __name__ == '__main__':
    setup_database()
