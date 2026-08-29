"""
FastAPI Authentication Service
Run this separately from Streamlit
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from dotenv import load_dotenv

from database.models import db
from auth.email_service import email_service

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="IntelligentInsightAnalyzer Auth Service")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Auth Endpoints
# ============================================================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "auth"}


@app.post("/auth/send-otp")
def send_otp(data: dict):
    """Send OTP to email"""
    try:
        email = data.get("email", "").lower().strip()
        
        if not email or "@" not in email or "." not in email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        db.create_user(email)
        otp_code = email_service.generate_otp()
        db.save_otp(email, otp_code, validity_minutes=5)
        email_sent = email_service.send_otp_email(email, otp_code)
        
        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {
            "success": True,
            "message": f"OTP sent to {email}. Valid for 5 minutes."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/verify-otp")
def verify_otp(data: dict):
    """Verify OTP and create session"""
    try:
        email = data.get("email", "").lower().strip()
        otp_code = data.get("otp", "").strip()
        
        if not db.verify_otp(email, otp_code):
            raise HTTPException(status_code=401, detail="Invalid or expired OTP")
        
        session_token = str(uuid.uuid4())
        db.create_session(email, session_token, validity_hours=24)
        
        return {
            "success": True,
            "message": "Login successful",
            "session_token": session_token,
            "email": email
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/verify-session")
def verify_session(data: dict):
    """Verify session token"""
    try:
        session_token = data.get("email", "")
        
        user_info = db.verify_session(session_token)
        
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        return {
            "success": True,
            "email": user_info['email']
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/logout")
def logout(data: dict):
    """Logout user"""
    try:
        session_token = data.get("email", "")
        db.invalidate_session(session_token)
        
        return {
            "success": True,
            "message": "Logged out successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/user/{email}")
def get_user(email: str):
    """Get user information"""
    try:
        user = db.get_user(email.lower().strip())
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "user": user
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  IntelligentInsightAnalyzer - Auth Service                ║
    ║  Running on: http://localhost:8000                         ║
    ║  Docs: http://localhost:8000/docs                          ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
