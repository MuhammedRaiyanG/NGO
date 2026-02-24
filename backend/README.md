# Hope Foundation Backend

Flask REST API backend for the Hope Foundation NGO website.

## Features

- Admin authentication and authorization
- Volunteer registration management
- Contact form submissions handling
- Donation tracking and statistics
- Impact metrics management (admin only)
- JWT token-based security

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file with your settings:
- `FLASK_ENV`: Set to 'development' or 'production'
- `JWT_SECRET_KEY`: Change this to a secure random string in production

### 3. Initialize Database

The database is automatically created when you first run the app. Default admin credentials:
- Username: `admin`
- Password: `admin123`

**Important:** Change these credentials after first login!

### 4. Run the Server

```bash
python app.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Admin login
- `POST /api/auth/register` - Register new admin
- `GET /api/auth/profile` - Get current admin profile (requires JWT)

### Volunteers
- `POST /api/volunteers/` - Submit volunteer registration
- `GET /api/volunteers/` - Get all registrations (admin only)
- `GET /api/volunteers/<id>` - Get specific volunteer (admin only)
- `PUT /api/volunteers/<id>` - Update volunteer status (admin only)
- `DELETE /api/volunteers/<id>` - Delete volunteer (admin only)

### Contact Messages
- `POST /api/contacts/` - Submit contact form
- `GET /api/contacts/` - Get all messages (admin only)
- `GET /api/contacts/<id>` - Get specific message (admin only)
- `PUT /api/contacts/<id>` - Update message status (admin only)
- `DELETE /api/contacts/<id>` - Delete message (admin only)

### Donations
- `POST /api/donations/` - Record a donation
- `GET /api/donations/` - Get all donations (admin only)
- `GET /api/donations/<id>` - Get specific donation (admin only)
- `PUT /api/donations/<id>` - Update donation status (admin only)
- `GET /api/donations/stats` - Get donation statistics (admin only)

### Admin Dashboard
- `GET /api/admin/dashboard` - Get dashboard overview (admin only)
- `GET /api/admin/metrics` - Get all impact metrics (admin only)
- `POST /api/admin/metrics` - Create new metric (admin only)
- `PUT /api/admin/metrics/<name>` - Update metric (admin only)
- `DELETE /api/admin/metrics/<name>` - Delete metric (admin only)

### Health Check
- `GET /api/health` - Check API status

## Example Usage

### Login as Admin

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "admin": {
    "id": 1,
    "username": "admin",
    "email": "admin@hope.ngo",
    "created_at": "2026-02-24T12:00:00"
  }
}
```

### Submit Volunteer Registration

```bash
curl -X POST http://localhost:5000/api/volunteers/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+91 9876543210",
    "interested_area": "women_safety"
  }'
```

### Submit Contact Form

```bash
curl -X POST http://localhost:5000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "message": "I want to help with your mission"
  }'
```

## Database Models

- **Admin**: Store admin users with password hashing
- **Volunteer**: Store volunteer registration submissions
- **ContactMessage**: Store contact form submissions
- **Donation**: Store donation records
- **ImpactMetric**: Store editable impact metrics for the website

## Security Notes

- All admin endpoints require JWT authentication
- Passwords are hashed using werkzeug security utilities
- CORS is enabled for frontend communication
- Make sure to change default admin password in production
- Use environment variables for sensitive configuration

## Development

The backend uses:
- Flask: Web framework
- SQLAlchemy: ORM for database
- Flask-JWT-Extended: JWT authentication
- Flask-CORS: Cross-origin resource sharing

## Production Deployment

Before deploying to production:

1. Change `JWT_SECRET_KEY` to a secure random string
2. Set `FLASK_ENV` to 'production'
3. Change default admin password
4. Use a production database (PostgreSQL recommended)
5. Set up proper error logging and monitoring
6. Enable HTTPS
7. Configure proper CORS origins

## Support

For issues or questions, contact: hello@hope.ngo
