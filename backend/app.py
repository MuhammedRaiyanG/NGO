import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config import config
from models import db, Admin, Volunteer, ContactMessage, Donation, ImpactMetric, Sustainer
import json

load_dotenv()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from routes import auth_routes, volunteer_routes, contact_routes, donation_routes, admin_routes, sustainer_routes
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(volunteer_routes.bp)
    app.register_blueprint(contact_routes.bp)
    app.register_blueprint(donation_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(sustainer_routes.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        # Create default admin if doesn't exist
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@hope.ngo')
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            
            # Add default impact metrics
            metrics = [
                ImpactMetric(metric_name='women_safety_centers', metric_value=18, metric_description='women safety centers'),
                ImpactMetric(metric_name='rehab_success_stories', metric_value=1450, metric_description='rehab success stories'),
                ImpactMetric(metric_name='blood_units_yearly', metric_value=4200, metric_description='blood units/year'),
                ImpactMetric(metric_name='legal_aid_cases', metric_value=312, metric_description='legal aid cases'),
            ]
            db.session.add_all(metrics)
            db.session.commit()
    
    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'Hope Foundation API is running'}, 200
    
    # Serve index.html at root and /index.html
    @app.route('/', methods=['GET'])
    @app.route('/index.html', methods=['GET'])
    def serve_index():
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return send_from_directory(parent_dir, 'index.html')

    # Serve uploaded files from backend/uploads
    @app.route('/uploads/<path:filename>', methods=['GET'])
    def serve_uploads(filename):
        upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
        return send_from_directory(upload_dir, filename)

    # Public team endpoint (reads backend/team.json)
    @app.route('/api/team', methods=['GET'])
    def public_team():
        team_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'team.json')
        if not os.path.exists(team_path):
            return {'team': []}, 200
        with open(team_path, 'r', encoding='utf-8') as f:
            team = json.load(f)
        return {'team': team}, 200
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
