"""
FastAPI Authentication Service
Run this separately from Streamlit
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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
# Request/Response Models
# ============================================================================

class EmailRequest(BaseModel):
    """Request model for OTP sending"""
    email: str


class OTPVerifyRequest(BaseModel):
    """Request model for OTP verification"""
    email: str
    otp: str


class AuthResponse(BaseModel):
    """Response model for authentication"""
    success: bool
    message: str
    session_token: Optional[str] = None
    email: Optional[str] = None


# ============================================================================
# Auth Endpoints
# ============================================================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "auth"}


@app.post("/auth/send-otp")
def send_otp(request: EmailRequest):
    """
    Send OTP to email
    
    Args:
        email: User email address
    
    Returns:
        Success message
    """
    try:
        email = request.email.lower().strip()
        
        # Validate email format
        if '@' not in email or '.' not in email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Create user if doesn't exist
        db.create_user(email)
        
        # Generate OTP
        otp_code = email_service.generate_otp()
        
        # Save OTP to database
        db.save_otp(email, otp_code, validity_minutes=5)
        
        # Send email
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
def verify_otp(request: OTPVerifyRequest):
    """
    Verify OTP and create session
    
    Args:
        email: User email
        otp: OTP code
    
    Returns:
        Session token if successful
    """
    try:
        email = request.email.lower().strip()
        otp_code = request.otp.strip()
        
        # Verify OTP
        if not db.verify_otp(email, otp_code):
            raise HTTPException(status_code=401, detail="Invalid or expired OTP")
        
        # Create session token
        session_token = str(uuid.uuid4())
        
        # Save session
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
def verify_session(request: EmailRequest):
    """
    Verify session token
    
    Args:
        email: User email (used as session identifier)
    
    Returns:
        User info if session valid
    """
    try:
        session_token = request.email  # Passed as email field for simplicity
        
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
def logout(request: EmailRequest):
    """
    Logout user (invalidate session)
    
    Args:
        email: Session token
    
    Returns:
        Success message
    """
    try:
        session_token = request.email  # Passed as email field
        
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
        "auth_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
