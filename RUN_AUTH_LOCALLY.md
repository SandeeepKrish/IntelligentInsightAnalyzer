# Running Authentication Locally

## Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Step 1: Start FastAPI Auth Server

Open Terminal 1:
```bash
cd backend
python -m auth.auth_service
```

Expected output:
```
╔════════════════════════════════════════════════════════════╗
║  IntelligentInsightAnalyzer - Auth Service                ║
║  Running on: http://localhost:8000                         ║
║  Docs: http://localhost:8000/docs                          ║
╚════════════════════════════════════════════════════════════╝
```

## Step 2: Start Streamlit Frontend

Open Terminal 2:
```bash
cd frontend
streamlit run app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

## Step 3: Test Login Flow

1. Open `http://localhost:8501` in browser
2. Go to **Login** page (in sidebar)
3. Enter any email (e.g., `test@example.com`)
4. Click **Send OTP**
5. Check Terminal 1 for OTP code (will be printed)
6. Copy OTP and enter in Streamlit
7. Click **Verify OTP**
8. ✅ Should see login success!
9. Click "Main App" to go to dashboard
10. See profile badge with first letter of email

## Testing Features

### Send OTP
- Tests email validation
- Creates user in database
- Generates and saves OTP
- Prints OTP to console (mock mode)

### Verify OTP
- Validates OTP format
- Checks OTP expiration (5 minutes)
- Creates session token
- Marks OTP as used

### Profile Badge
- Shows first letter of email in colored circle
- Displays email address
- Shows "Logged in" status
- Logout button to end session

### Logout
- Invalidates session token
- Clears authentication state
- Redirects to login page

## Troubleshooting

### "Cannot connect to auth server"
- Make sure FastAPI is running on http://localhost:8000
- Check Terminal 1 for errors

### "Invalid or expired OTP"
- OTP valid for only 5 minutes
- Check that you copied the OTP correctly
- OTP is printed in Terminal 1

### Pages not showing
- Make sure you're logged in first
- Go to Login page before accessing Main App

## Database

- SQLite database: `backend/src/database/auth.db`
- Auto-created on first run
- Contains: users, otps, sessions tables

## Next Steps

1. ✅ Test locally with mock emails
2. To use real Gmail emails (optional):
   - Get App Password: https://support.google.com/accounts/answer/185833
   - Add to .env:
     ```
     GMAIL_USER=your-email@gmail.com
     GMAIL_APP_PASSWORD=your-app-password
     ```
   - Update `email_service.py`: change `use_mock=False`
3. Deploy to Streamlit Cloud with FastAPI backend
