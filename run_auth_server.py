"""
Run FastAPI auth server from root directory
"""

import sys
import os

# Add backend src to path
backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src)

# Now import and run
from auth.auth_service import app
import uvicorn

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  IntelligentInsightAnalyzer - Auth Service                ║
    ║  Running on: http://localhost:8000                         ║
    ║  Docs: http://localhost:8000/docs                          ║
    ║                                                            ║
    ║  To login:                                                 ║
    ║  1. Open http://localhost:8501 in browser                 ║
    ║  2. Go to Login page                                       ║
    ║  3. Enter email and OTP will be sent to your email        ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
