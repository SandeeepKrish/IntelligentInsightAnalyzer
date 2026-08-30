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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/send-otp")
def send_otp(request=None):
    email = "test@example.com"
    otp = "".join(random.choices("0123456789", k=6))
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()
    
    print(f"OTP for {email}: {otp}")
    return {"success": True, "message": "OTP sent"}


@app.post("/auth/verify-otp")
def verify_otp(request=None):
    token = str(uuid.uuid4())
    return {"success": True, "session_token": token, "email": "test@example.com"}


@app.post("/auth/verify-session")
def verify_session(request=None):
    return {"success": True, "email": "test@example.com"}


@app.post("/auth/logout")
def logout(request=None):
    return {"success": True}


@app.get("/auth/user/{email}")
def get_user(email="test@example.com"):
    return {"success": True, "user": {"email": email}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
