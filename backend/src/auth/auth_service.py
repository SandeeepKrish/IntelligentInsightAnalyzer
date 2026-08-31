from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import uuid
import random
from datetime import datetime, timedelta
from .email_service import email_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), '../database/auth.db')
_DB_INITIALIZED = False


def init_db():
    """Initialize SQLite database with required tables (lazy load)"""
    global _DB_INITIALIZED
    if _DB_INITIALIZED:
        return
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        email TEXT UNIQUE, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        last_login TIMESTAMP, 
        is_active BOOLEAN DEFAULT 1
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS otps (
        id INTEGER PRIMARY KEY, 
        email TEXT, 
        otp_code TEXT, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        expires_at TIMESTAMP, 
        is_used BOOLEAN DEFAULT 0, 
        used_at TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY, 
        email TEXT, 
        session_token TEXT UNIQUE, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        expires_at TIMESTAMP, 
        is_active BOOLEAN DEFAULT 1
    )''')
    conn.commit()
    conn.close()
    _DB_INITIALIZED = True


@app.get("/")
def root():
    init_db()  # Lazy initialize on first request
    return {"status": "ok", "service": "IntelligentInsightAnalyzer Auth", "message": "Backend is running", "docs": "/docs"}


@app.get("/health")
def health():
    init_db()  # Lazy initialize on first request
    return {"status": "ok"}


@app.post("/auth/send-otp")
async def send_otp(request: Request):
    """Send OTP to user email"""
    try:
        init_db()  # Lazy initialize
        body = await request.json()
        email = body.get("email", "").lower().strip()
        
        if not email or "@" not in email:
            return {"success": False, "message": "Invalid email address"}
        
        # Create user if doesn't exist
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
        conn.commit()
        
        # Generate OTP
        otp = "".join(random.choices("0123456789", k=6))
        expires = (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        
        # Save OTP to database
        c.execute("INSERT INTO otps (email, otp_code, expires_at) VALUES (?, ?, ?)", (email, otp, expires))
        conn.commit()
        conn.close()
        
        # Send OTP via email service (real SMTP or mock mode)
        email_sent = email_service.send_otp_email(email, otp)
        
        if email_sent:
            return {"success": True, "message": "OTP sent successfully"}
        else:
            return {"success": True, "message": "OTP generated (email service unavailable - check backend logs)"}
    
    except Exception as e:
        print(f"Error in send_otp: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


@app.post("/auth/verify-otp")
async def verify_otp(request: Request):
    """Verify OTP and create session"""
    try:
        init_db()  # Lazy initialize
        body = await request.json()
        email = body.get("email", "").lower().strip()
        otp = body.get("otp", "").strip()
        
        if not email or not otp:
            return {"success": False, "message": "Email and OTP required"}
        
        # Check OTP in database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM otps WHERE email = ? AND otp_code = ? AND is_used = 0 ORDER BY created_at DESC LIMIT 1", 
            (email, otp)
        )
        row = c.fetchone()
        
        if not row:
            conn.close()
            return {"success": False, "message": "Invalid OTP"}
        
        # Check if OTP is expired (row[4] is expires_at column)
        expires_at = datetime.fromisoformat(row[4])
        if datetime.utcnow() > expires_at:
            conn.close()
            return {"success": False, "message": "OTP has expired"}
        
        # Mark OTP as used
        c.execute("UPDATE otps SET is_used = 1, used_at = CURRENT_TIMESTAMP WHERE id = ?", (row[0],))
        conn.commit()
        
        # Create session token
        token = str(uuid.uuid4())
        expires = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        c.execute(
            "INSERT INTO sessions (email, session_token, expires_at) VALUES (?, ?, ?)", 
            (email, token, expires)
        )
        conn.commit()
        
        # Update last login
        c.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        
        print(f"✅ OTP verified for {email}. Session created: {token[:8]}...")
        return {
            "success": True, 
            "session_token": token, 
            "email": email,
            "message": "Login successful"
        }
    
    except Exception as e:
        print(f"Error in verify_otp: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


@app.post("/auth/verify-session")
async def verify_session(request: Request):
    """Verify if session token is valid"""
    try:
        init_db()  # Lazy initialize
        body = await request.json()
        token = body.get("session_token", "").strip()  # FIX: was getting "email" instead of session_token
        
        if not token:
            return {"success": False, "message": "Session token required"}
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM sessions WHERE session_token = ? AND is_active = 1", 
            (token,)
        )
        row = c.fetchone()
        conn.close()
        
        if not row:
            return {"success": False, "message": "Invalid session"}
        
        # Check if session expired (row[4] is expires_at)
        expires_at = datetime.fromisoformat(row[4])
        if datetime.utcnow() > expires_at:
            return {"success": False, "message": "Session expired"}
        
        print(f"✅ Session verified for {row[1]}")
        return {"success": True, "email": row[1]}
    
    except Exception as e:
        print(f"Error in verify_session: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


@app.post("/auth/logout")
async def logout(request: Request):
    """Invalidate session"""
    try:
        init_db()  # Lazy initialize
        body = await request.json()
        token = body.get("session_token", "").strip()
        
        if not token:
            return {"success": False, "message": "Session token required"}
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE sessions SET is_active = 0 WHERE session_token = ?", (token,))
        conn.commit()
        conn.close()
        
        print(f"✅ Session logged out: {token[:8]}...")
        return {"success": True, "message": "Logged out successfully"}
    
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


@app.get("/auth/user/{email}")
def get_user(email: str):
    """Get user information"""
    try:
        init_db()  # Lazy initialize
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, email, created_at, last_login FROM users WHERE email = ?", (email.lower().strip(),))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return {"success": False, "message": "User not found"}
        
        return {
            "success": True, 
            "user": {
                "id": row[0], 
                "email": row[1],
                "created_at": row[2],
                "last_login": row[3]
            }
        }
    except Exception as e:
        print(f"Error in get_user: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

