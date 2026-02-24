# 🔐 Admin Login & Edit Features Guide

## How It Works

### **When NOT Logged In (Default)**
- ✅ Users can see the website normally
- ✅ All forms are visible and working
- ❌ **NO edit buttons appear anywhere**
- ❌ **No admin panel visible**
- ❌ **Cannot edit metrics**

### **When Logged In as Admin**
- ✅ Users still see the website
- ✅ **Edit buttons now appear on all editable content**
- ✅ **Admin panel is visible**
- ✅ **Can edit metrics in real-time**
- ✅ **Can view all submissions**

---

## Step-by-Step Usage

### Step 1: Start Website
Double-click `START.bat` and the website opens

### Step 2: Click ADMIN Button
Located in top-right corner of navigation bar

### Step 3: Login
Enter credentials:
- Username: `admin`
- Password: `admin123`

### Step 4: See Edit Options
Now you'll see **[edit]** buttons on:
- ✏️ Impact metrics (18, 1,450, 4.2k, 312)
- ✏️ Bank transfer details
- ✏️ QR code information
- ✏️ Contact information
- ✏️ Tax/certification info

### Step 5: Click Any [edit]
A popup appears to update that information

### Step 6: Logout
Click ADMIN button again to logout
- Edit buttons **disappear immediately**
- Admin panel **disappears**
- Everything goes back to normal

---

## What Users See

### **Logged Out View**
```
Navigation: HOME | ABOUT | IMPACT | DONATE | TEAM | CONTACT | [ADMIN]
Impact Cards: 18 | 1,450 | 4.2k | 312
(NO edit buttons visible)
Donation Box: Bank, UPI, Monthly (NO edit options)
Contact Info: Address, Phone, Email (NO edit options)
Footer: Normal content only
```

### **Logged In View (Admin)**
```
Navigation: HOME | ABOUT | IMPACT | DONATE | TEAM | CONTACT | [ADMIN ON] ← Changes color/icon
Impact Cards: 18 [edit] | 1,450 [edit] | 4.2k [edit] | 312 [edit]
Donation Box: Bank, UPI, Monthly + [edit]s visible
Contact Info: Address, Phone, Email + [edit]s visible
Admin Panel: APPEARS with dashboard showing stats
Footer: Shows admin options
```

---

## Edit Options Visibility

### When Logged Out: Hidden
```javascript
.edit-option { display: none !important; }
```

### When Logged In: Visible
```javascript
body.show-admin .edit-option { display: block !important; }
```

---

## Security Features

✅ **Credentials Not Exposed**
- Password never shown on page
- Edit buttons only show when authenticated
- Session stored in localStorage only
- Token required for all API calls

✅ **Non-Admin Users See Nothing**
- Edit buttons completely hidden
- Admin panel never appears
- No sensitive options visible
- Clean public website experience

✅ **Quick Logout**
- One click to logout
- All admin features disappear
- Token removed from browser

---

## Features Available Only When Logged In

**Content Editing:**
- Edit impact metrics ✏️
- Edit bank details ✏️
- Edit tax information ✏️
- Edit contact details ✏️

**Data Management:**
- View volunteer registrations
- View contact messages
- Track donations
- Export reports
- Manage submissions

**Admin Dashboard:**
- Live statistics
- Pending requests count
- Unread messages count
- Total donations raised

---

## Testing It Out

1. **Open website** - No edit buttons
2. **Click ADMIN** - Login modal appears
3. **Enter admin/admin123** - You're logged in
4. **Look at metrics** - Edit buttons now appear!
5. **Click [edit]** on any metric - Popup appears
6. **Change value** - Updated successfully
7. **Click ADMIN again** - Logout immediately
8. **Look at metrics** - Edit buttons gone!

---

## Important Notes

⚠️ **Session Persistence**
- Login status persists if you refresh the page
- Stored in browser's localStorage
- Logout clears everything
- Private browsing mode won't remember login

⚠️ **Security**
- Change default password in production
- Use HTTPS in production
- Don't leave admin sessions open
- Use strong passwords

✅ **Best Practice**
- Logout when finished editing
- Use different password than other accounts
- Regularly review submissions
- Keep backups of edits

---

## Troubleshooting

**Edit button not appearing after login?**
- Refresh the page (F5)
- Check if you're truly logged in
- Look for "ADMIN ON" text in button

**Edit button appearing when logged out?**
- Clear browser cache
- Clear localStorage
- Try private/incognito window

**Can't logout/login?**
- Check backend is running
- Try refreshing page
- Check browser console (F12) for errors

---

## Summary

| State | Edit Buttons | Admin Panel | View Submissions |
|-------|------------|-------------|------------------|
| **Logged Out** | ❌ Hidden | ❌ Hidden | ❌ No |
| **Logged In** | ✅ Visible | ✅ Visible | ✅ Yes |

**Simple: Login to edit, Logout when done!** 🔒
