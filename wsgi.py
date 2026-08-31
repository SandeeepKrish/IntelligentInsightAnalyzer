from backend.src.auth.auth_service import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(__import__('os').environ.get("PORT", 10000)))


