# Quick Start Guide - Hope Foundation Backend

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Step 1: Install Dependencies

Open PowerShell in the `backend` folder and run:

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Flask-CORS (cross-origin support)
- Flask-JWT-Extended (authentication)
- python-dotenv (environment variables)

## Step 2: Initialize Database

Run the setup script to create the database and initialize data:

```powershell
python setup_db.py
```

This will:
- Create SQLite database (`hope_foundation.db`)
- Create default admin user (username: `admin`, password: `admin123`)
- Initialize impact metrics

## Step 3: Start the Backend Server

```powershell
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

The server is now running at: **http://localhost:5000**

## Step 4: Update Frontend

Make sure your `index.html` is configured to use the backend:
- The JavaScript code automatically connects to `http://localhost:5000/api`
- Open `index.html` in a browser to test

## Testing the API

### 1. Check API Health
```powershell
curl http://localhost:5000/api/health
```

### 2. Login as Admin
```powershell
curl -X POST http://localhost:5000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"admin","password":"admin123"}'
```

### 3. Test Volunteer Registration
```powershell
curl -X POST http://localhost:5000/api/volunteers/ `
  -H "Content-Type: application/json" `
  -d '{
    "full_name":"John Doe",
    "email":"john@example.com",
    "phone":"+91 9876543210",
    "interested_area":"women_safety"
  }'
```

## Stopping the Server

Press `Ctrl + C` in the PowerShell window where the server is running.

## Common Issues

### "ModuleNotFoundError: No module named 'flask'"
- Make sure you ran `pip install -r requirements.txt` first
- Check that pip is using the correct Python environment

### "Address already in use"
- Another application is using port 5000
- Change the port in `app.py` line: `app.run(..., port=5001)`
- Or kill the existing process

### Frontend can't connect to backend
- Make sure backend is running (you should see the Flask message)
- Check that frontend is trying to connect to `http://localhost:5000`
- Look at browser console for CORS or connection errors

### Database locked errors
- Make sure you only have one instance of `app.py` running
- Delete `hope_foundation.db` to start fresh (you'll lose data)

## File Structure

```
backend/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Database models
├── setup_db.py         # Database initialization
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── .gitignore          # Git ignore file
├── README.md           # Full documentation
├── routes/             # API route blueprints
│   ├── auth_routes.py
│   ├── volunteer_routes.py
│   ├── contact_routes.py
│   ├── donation_routes.py
│   └── admin_routes.py
└── hope_foundation.db  # SQLite database (created after setup)
```

## Next Steps

1. Change the default admin password in production
2. Configure the database to use PostgreSQL for production
3. Set up HTTPS
4. Deploy to a production server (Heroku, AWS, DigitalOcean, etc.)
5. Configure email notifications for new messages

## Support

If you encounter issues:
1. Check that Python is properly installed: `python --version`
2. Verify port 5000 is available: `netstat -ano | findstr :5000`
3. Check the Flask server logs for error messages
4. Review the README.md for more detailed documentation

---

**Ready to go!** Your backend is now running and ready to handle forms and admin requests.
