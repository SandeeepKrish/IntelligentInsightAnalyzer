from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from dotenv import load_dotenv

from database.models import db
from auth.email_service import email_service

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/send-otp")
async def send_otp(request):
    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        
        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Invalid email")
        
        db.create_user(email)
        otp = email_service.generate_otp()
        db.save_otp(email, otp)
        email_service.send_otp_email(email, otp)
        
        return {"success": True, "message": "OTP sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/verify-otp")
async def verify_otp(request):
    try:
        body = await request.json()
        email = body.get("email", "").lower().strip()
        otp = body.get("otp", "").strip()
        
        if not db.verify_otp(email, otp):
            raise HTTPException(status_code=401, detail="Invalid OTP")
        
        token = str(uuid.uuid4())
        db.create_session(email, token)
        
        return {"success": True, "session_token": token, "email": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/verify-session")
async def verify_session(request):
    try:
        body = await request.json()
        token = body.get("email", "")
        
        user = db.verify_session(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid session")
        
        return {"success": True, "email": user["email"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/logout")
async def logout(request):
    try:
        body = await request.json()
        token = body.get("email", "")
        db.invalidate_session(token)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/user/{email}")
def get_user(email: str):
    try:
        user = db.get_user(email.lower().strip())
        if not user:
            raise HTTPException(status_code=404, detail="Not found")
        return {"success": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
