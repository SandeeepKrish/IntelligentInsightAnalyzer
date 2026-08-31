from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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

# In-memory storage (fast, no I/O)
users_db = {}
otps_db = {}
sessions_db = {}


@app.get("/")
def root():
    return {"status": "ok", "service": "IntelligentInsightAnalyzer Auth", "message": "Backend is running", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/send-otp")
async def send_otp(request: Request):
    """Send OTP to user email"""
    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        
        if not email or "@" not in email:
            return {"success": False, "message": "Invalid email address"}
        
        # Create user if doesn't exist
        if email not in users_db:
            users_db[email] = {"created_at": datetime.utcnow().isoformat()}
        
        # Generate OTP
        otp = "".join(random.choices("0123456789", k=6))
        expires = datetime.utcnow() + timedelta(minutes=5)
        
        # Save OTP
        otps_db[email] = {"otp": otp, "expires_at": expires.isoformat(), "used": False}
        
        # Send OTP
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
        body = await request.json()
        email = body.get("email", "").lower().strip()
        otp = body.get("otp", "").strip()
        
        if not email or not otp:
            return {"success": False, "message": "Email and OTP required"}
        
        # Check OTP
        if email not in otps_db:
            return {"success": False, "message": "Invalid OTP"}
        
        otp_data = otps_db[email]
        
        if otp_data["otp"] != otp:
            return {"success": False, "message": "Invalid OTP"}
        
        if otp_data["used"]:
            return {"success": False, "message": "OTP already used"}
        
        # Check expiration
        expires_at = datetime.fromisoformat(otp_data["expires_at"])
        if datetime.utcnow() > expires_at:
            return {"success": False, "message": "OTP has expired"}
        
        # Mark OTP as used
        otp_data["used"] = True
        
        # Create session
        token = str(uuid.uuid4())
        expires = datetime.utcnow() + timedelta(hours=24)
        sessions_db[token] = {"email": email, "expires_at": expires.isoformat(), "active": True}
        
        # Update user last login
        users_db[email]["last_login"] = datetime.utcnow().isoformat()
        
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
        body = await request.json()
        token = body.get("session_token", "").strip()
        
        if not token:
            return {"success": False, "message": "Session token required"}
        
        if token not in sessions_db:
            return {"success": False, "message": "Invalid session"}
        
        session_data = sessions_db[token]
        
        if not session_data["active"]:
            return {"success": False, "message": "Session inactive"}
        
        # Check expiration
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        if datetime.utcnow() > expires_at:
            return {"success": False, "message": "Session expired"}
        
        print(f"✅ Session verified for {session_data['email']}")
        return {"success": True, "email": session_data["email"]}
    
    except Exception as e:
        print(f"Error in verify_session: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


@app.post("/auth/logout")
async def logout(request: Request):
    """Invalidate session"""
    try:
        body = await request.json()
        token = body.get("session_token", "").strip()
        
        if not token:
            return {"success": False, "message": "Session token required"}
        
        if token in sessions_db:
            sessions_db[token]["active"] = False
        
        print(f"✅ Session logged out: {token[:8]}...")
        return {"success": True, "message": "Logged out successfully"}
    
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


@app.get("/auth/user/{email}")
def get_user(email: str):
    """Get user information"""
    try:
        email = email.lower().strip()
        
        if email not in users_db:
            return {"success": False, "message": "User not found"}
        
        user = users_db[email]
        return {
            "success": True, 
            "user": {
                "email": email,
                "created_at": user.get("created_at"),
                "last_login": user.get("last_login")
            }
        }
    except Exception as e:
        print(f"Error in get_user: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
