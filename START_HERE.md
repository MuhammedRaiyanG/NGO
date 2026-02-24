# Hope Foundation - Quick Start Guide

## Easy 3-Step Setup

### Step 1: Start the Backend (Terminal 1)
Open PowerShell in `d:\NGO\backend` and run:
```powershell
& "C:\Users\ELCOT\AppData\Local\Programs\Python\Python311\python.exe" app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Leave this terminal open!**

---

### Step 2: Open the Website (Terminal 2)
Open a NEW PowerShell window and run:
```powershell
cd d:\NGO
Start-Process "http://localhost:5000/index.html"
```

Or simply open `index.html` in your browser:
- File → Open → `d:\NGO\index.html`

---

### Step 3: Test Admin Panel
1. Click **ADMIN** button (top right)
2. Login with:
   - **Username:** `admin`
   - **Password:** `admin123`

---

## What You Can Do Now:

✅ **Volunteer Registration** - Fill form, data saves automatically
✅ **Contact Form** - Send messages, stored in database  
✅ **Admin Panel** - View all submissions and edit metrics
✅ **Donation Tracking** - Record donations

---

## Shortcut Script

Create a file called `RUN.bat` in `d:\NGO` with this content:

```batch
@echo off
start "Backend Server" cmd /k "cd d:\NGO\backend && C:\Users\ELCOT\AppData\Local\Programs\Python\Python311\python.exe app.py"
timeout /t 3
start "Website" http://localhost:5000/index.html
```

Then double-click `RUN.bat` to start everything!

---

## Default Admin Credentials
- **Username:** admin
- **Password:** admin123

⚠️ Change these in production!

---

## Files Created

- `d:\NGO\index.html` - Main website
- `d:\NGO\backend\app.py` - Flask backend
- `d:\NGO\backend\models.py` - Database models
- `d:\NGO\backend\hopes_foundation.db` - SQLite database

---

## Troubleshooting

**Backend won't start?**
```powershell
cd d:\NGO\backend
& "C:\Users\ELCOT\AppData\Local\Programs\Python\Python311\python.exe" app.py
```

**Website can't connect to backend?**
- Make sure backend terminal is running
- Check that you see "Running on http://127.0.0.1:5000"

**Forms not submitting?**
- Open browser Developer Tools (F12)
- Check Console tab for errors
- Make sure backend is running

---

## API Endpoints

Backend API is at: `http://localhost:5000/api`

Available endpoints:
- `POST /api/volunteers/` - New volunteer
- `POST /api/contacts/` - New contact message
- `POST /api/auth/login` - Admin login
- `GET /api/admin/dashboard` - Dashboard (requires login)

---

**You're all set! Start with Step 1 above.**
