# 🏦 Account Management Access Guide

## 🚀 **Quick Access Steps**

### **Method 1: Using Demo Credentials (Recommended)**
1. **Go to Login Page**: http://localhost:8080/login
2. **Click "Use Demo Credentials"** button (auto-fills email and API key)
3. **Click "Sign In"** button
4. **You'll be redirected to Developer Dashboard**
5. **Click "Manage Accounts"** button in the Documentation section
6. **Account Management page will load with your data!**

### **Method 2: Direct Navigation (if already logged in)**
1. **Go directly to**: http://localhost:8080/account-management
2. **If not logged in**, you'll see authentication required message
3. **Click "Login with API Key"** to go to login page
4. **Follow Method 1 steps**

### **Method 3: Register New Account**
1. **Go to Registration**: http://localhost:8080/register
2. **Complete the registration form**
3. **Copy your API key from success page**
4. **Go to Login**: http://localhost:8080/login
5. **Enter your email and API key**
6. **Access account management**

## 🔑 **Demo Credentials**
```
Email: system-test1757935897@rowell-infra.com
API Key: ri_GPu9zJuP_9pAhaXPgU8TcmYA_NFVNj_unPv2Ki7fpYc
```

## 🎯 **What You'll See in Account Management**

### **Overview Cards:**
- **Total Accounts**: Number of accounts you've created
- **Active Accounts**: Number of active accounts
- **Total Transfers**: Number of transfers made
- **Pending Transfers**: Number of pending transfers

### **Account Management Section:**
- **List of Accounts**: All your created accounts
- **Account Details**: Network, environment, status, KYC status
- **Copy Account ID**: Click copy button to copy account ID
- **Create New Account**: Button to create additional accounts

### **Transfer Management Section:**
- **Recent Transfers**: List of your recent transfers
- **Create Transfer Form**: Form to create new transfers
- **Transfer Status**: Track transfer status (pending, success, failed)

## 🚨 **Troubleshooting**

### **If you can't access the page:**

1. **Check Authentication:**
   - Open browser Developer Tools (F12)
   - Go to Application/Storage tab
   - Check localStorage for `rowell_api_key`
   - If missing, you need to login first

2. **Check Console Errors:**
   - Open browser Developer Tools (F12)
   - Go to Console tab
   - Look for any JavaScript errors
   - Refresh page if needed

3. **Verify Services:**
   - Frontend: http://localhost:8080 (should show landing page)
   - Backend: http://localhost:8000/health (should return status)

4. **Clear Browser Data:**
   - Clear localStorage
   - Clear cookies
   - Try logging in again

### **If the page shows "Authentication Required":**
- You need to login first
- Use the demo credentials or your own API key
- Make sure the API key starts with "ri_"

### **If the page shows "Loading..." forever:**
- Check if backend is running on port 8000
- Check browser console for API errors
- Try refreshing the page

## 🎉 **Success Indicators**

You'll know it's working when you see:
- ✅ Account overview cards with numbers
- ✅ List of your accounts (if any created)
- ✅ Transfer history (if any transfers made)
- ✅ "Create Account" and "Create Transfer" buttons working
- ✅ Navigation working between pages

## 📱 **Navigation**

- **Back to Dashboard**: Click "← Back to Dashboard" button
- **Home**: Click "Rowell Infra" logo in top-left
- **Login**: Click "Login" in top navigation
- **Dashboard**: Click "Dashboard" in top navigation

## 🔧 **Technical Details**

- **Frontend**: React with TypeScript, running on port 8080
- **Backend**: FastAPI with SQLite, running on port 8000
- **Authentication**: API key stored in localStorage
- **Data**: Accounts and transfers fetched from backend API

---

**Need Help?** Check the browser console for errors or contact support!
