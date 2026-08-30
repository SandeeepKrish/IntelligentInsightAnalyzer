import sys
import os

# Add backend src to path for Render deployment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    from auth.auth_service import app
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback: try alternative import
    from backend.src.auth.auth_service import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

