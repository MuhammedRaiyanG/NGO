# Hope Foundation - Admin Panel Guide

## Login

1. Click **ADMIN** button (top right corner)
2. Enter credentials:
   - **Username:** `admin`
   - **Password:** `admin123`

---

## Admin Features

### 1. **Impact Metrics Editor** ⭐
Edit the impact numbers shown on the "Our Impact" section:

**Where:** Click on any metric card's **"edit"** link
- Women Safety Centers
- Rehab Success Stories  
- Blood Units/Year
- Legal Aid Cases

**How to Edit:**
1. Click the **[edit]** link on any impact card
2. A popup will appear with current value
3. Enter new number
4. Click **Save** to update
5. Page refreshes with new data

---

### 2. **Dashboard Overview**
View real-time statistics:

**Volunteers Section:**
- Pending registrations (awaiting approval)
- Total volunteers registered

**Contact Messages:**
- Unread messages count
- Total messages received

**Donations:**
- Total amount raised (confirmed only)
- Number of confirmed donations

---

### 3. **View Registrations**
See all volunteer registrations and manage them

**Access:**
1. Click **ADMIN** to login
2. Look for "registrations" box in admin panel
3. Shows: pending count & total count

**Features:**
- View all volunteer names
- Check email and phone
- See interested area
- Mark as approved/rejected

---

### 4. **View Contact Messages**
See all messages from the contact form

**Access:**
1. Admin Dashboard → "contact queries" box
2. Shows unread count

**Features:**
- Read all messages
- See sender name & email
- Mark as read/replied
- Delete messages

---

### 5. **Donation Tracking**
Track all donations received

**Access:**
1. Admin Dashboard → "DONATIONS" section
2. Shows total amount raised

**Features:**
- View all donations
- See donor names and amounts
- Track donation type (bank/UPI/monthly)
- Filter by status (pending/confirmed/failed)

---

## Making Changes

### **To Edit Impact Metrics:**
```
1. Click [edit] on any metric card
2. Enter new number
3. Click Save
4. Website updates automatically
```

**Example:**
- Admin sees: "edit" button on "Women Safety Centers" card
- Clicks it
- Enters: "25" (new number of centers)
- Clicks Save
- Website now shows: "25" instead of "18"

### **To View Submissions:**
```
1. Check admin dashboard for counts
2. Click on any section
3. See all entries with details
4. Manage/approve/delete as needed
```

---

## Reporting Features

### **Registrations Report**
- Export volunteer list to CSV
- Filter by status (pending/approved/rejected)
- See timestamps of registrations

### **Contact Report**
- All messages with sender details
- Timestamps of submissions
- Reply status tracking

### **Donation Report**
- Total amount received
- Average donation size
- Donations by type
- Monthly trends

---

## Important Notes

⚠️ **Security:**
- Change default password immediately in production
- Don't share admin credentials
- Keep admin token secure

✅ **Best Practices:**
- Update metrics monthly
- Review messages regularly
- Process applications within 48 hours
- Maintain accurate donation records

---

## Troubleshooting

**Edit button not working?**
- Make sure you're logged in as admin
- Refresh the page
- Check browser console for errors (F12)

**Changes not saving?**
- Verify backend is running
- Check if backend shows error in terminal
- Try logging out and back in

**Can't login?**
- Check username/password spelling
- Make sure to use exact credentials: admin / admin123
- See START.bat file for backup credentials

---

## Demo Data

The system comes pre-loaded with:
- **Admin User:** admin/admin123
- **Initial Metrics:**
  - Women Safety Centers: 18
  - Rehab Success Stories: 1,450
  - Blood Units/Year: 4,200
  - Legal Aid Cases: 312

---

## Quick Commands

**Start Backend:**
```powershell
Double-click START.bat
```

**Manual Start:**
```powershell
cd d:\NGO\backend
C:\Users\ELCOT\AppData\Local\Programs\Python\Python311\python.exe app.py
```

**Reset Database:**
```powershell
cd d:\NGO\backend
rm hope_foundation.db
python setup_db.py
```

---

**For more help, see START_HERE.md**
