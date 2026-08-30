from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import uuid
import random
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), '../database/auth.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, last_login TIMESTAMP, is_active BOOLEAN DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS otps (id INTEGER PRIMARY KEY, email TEXT, otp_code TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP, is_used BOOLEAN DEFAULT 0, used_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, email TEXT, session_token TEXT UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP, is_active BOOLEAN DEFAULT 1)''')
    conn.commit()
    conn.close()


init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": "IntelligentInsightAnalyzer Auth"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/send-otp")
async def send_otp(request):
    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        
        if not email or "@" not in email:
            return {"success": False, "message": "Invalid email"}
        
        # Create user
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
        conn.commit()
        
        # Generate OTP
        otp = "".join(random.choices("0123456789", k=6))
        expires = (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        
        # Save OTP
        c.execute("INSERT INTO otps (email, otp_code, expires_at) VALUES (?, ?, ?)", (email, otp, expires))
        conn.commit()
        conn.close()
        
        # Print to console (mock email)
        print(f"\n{'='*60}")
        print(f"OTP for {email}: {otp}")
        print(f"{'='*60}\n")
        
        return {"success": True, "message": "OTP sent"}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"success": False, "message": str(e)}


@app.post("/auth/verify-otp")
async def verify_otp(request):
    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        otp = body.get("otp", "").strip()
        
        # Check OTP
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM otps WHERE email = ? AND otp_code = ? AND is_used = 0 ORDER BY created_at DESC LIMIT 1", (email, otp))
        row = c.fetchone()
        
        if not row:
            conn.close()
            return {"success": False, "message": "Invalid OTP"}
        
        # Check expiration
        expires_at = datetime.fromisoformat(row[5])
        if datetime.utcnow() > expires_at:
            conn.close()
            return {"success": False, "message": "OTP expired"}
        
        # Mark as used
        c.execute("UPDATE otps SET is_used = 1, used_at = CURRENT_TIMESTAMP WHERE id = ?", (row[0],))
        conn.commit()
        
        # Create session
        token = str(uuid.uuid4())
        expires = (datetime.utcnow() + timedelta(hours=24)).isoformat()
        c.execute("INSERT INTO sessions (email, session_token, expires_at) VALUES (?, ?, ?)", (email, token, expires))
        conn.commit()
        conn.close()
        
        return {"success": True, "session_token": token, "email": email}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"success": False, "message": str(e)}


@app.post("/auth/verify-session")
async def verify_session(request):
    try:
        body = await request.json()
        token = body.get("email", "")
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM sessions WHERE session_token = ? AND is_active = 1", (token,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return {"success": False, "message": "Invalid session"}
        
        # Check expiration
        expires_at = datetime.fromisoformat(row[4])
        if datetime.utcnow() > expires_at:
            return {"success": False, "message": "Session expired"}
        
        return {"success": True, "email": row[1]}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.post("/auth/logout")
async def logout(request):
    try:
        body = await request.json()
        token = body.get("email", "")
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE sessions SET is_active = 0 WHERE session_token = ?", (token,))
        conn.commit()
        conn.close()
        
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.get("/auth/user/{email}")
def get_user(email: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return {"success": False, "message": "Not found"}
        
        return {"success": True, "user": {"id": row[0], "email": row[1]}}
    except Exception as e:
        return {"success": False, "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
