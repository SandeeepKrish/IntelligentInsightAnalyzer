"""
Login page for IntelligentInsightAnalyzer
Professional authentication with OTP via email
"""

import streamlit as st
import requests
import time
from datetime import datetime

# ============================================================================
# Suppress Browser Warnings
# ============================================================================

# Inject JavaScript to suppress feature detection warnings
st.markdown("""
<script>
// Suppress "Unrecognized feature" warnings from Permissions Policy checks
if (window.console) {
    const originalWarn = window.console.warn;
    const originalError = window.console.error;
    
    window.console.warn = function(...args) {
        const message = args[0]?.toString() || '';
        // Suppress known harmless warnings
        if (message.includes('Unrecognized feature') ||
            message.includes('ambient-light-sensor') ||
            message.includes('battery') ||
            message.includes('document-domain') ||
            message.includes('layout-animations') ||
            message.includes('legacy-image-formats') ||
            message.includes('oversized-images') ||
            message.includes('vr') ||
            message.includes('wake-lock')) {
            return;
        }
        originalWarn.apply(window.console, args);
    };
    
    window.console.error = function(...args) {
        const message = args[0]?.toString() || '';
        if (message.includes('Unrecognized feature')) {
            return;
        }
        originalError.apply(window.console, args);
    };
}
</script>
""", unsafe_allow_html=True)

# ============================================================================
# Configuration
# ============================================================================

# API endpoint
API_URL = "https://intelligentinsightanalyzer.onrender.com"
API_TIMEOUT = 5  # Reduced timeout - fail fast if backend unavailable


# ============================================================================
# Session State & Initialization
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "session_token" not in st.session_state:
        st.session_state.session_token = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "login_step" not in st.session_state:
        st.session_state.login_step = "email"  # email or otp


# ============================================================================
# Helper Functions
# ============================================================================

def send_otp_request(email):
    """Send OTP request to backend - fallback to local if unavailable"""
    try:
        response = requests.post(
            f"{API_URL}/auth/send-otp",
            json={"email": email},
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {"success": True, "message": data.get("message", "OTP sent successfully")}
            else:
                return {"success": False, "message": data.get("message", "Failed to send OTP")}
        else:
            return {"success": False, "message": f"Server error: {response.status_code}"}
    
    except requests.exceptions.ConnectionError:
        # Backend unavailable - use local/demo mode
        import random
        demo_otp = "".join(str(random.randint(0, 9)) for _ in range(6))
        st.session_state.demo_otp = demo_otp
        return {
            "success": True,
            "message": f"Demo Mode: OTP is {demo_otp} (valid for 5 mins)"
        }
    except requests.exceptions.Timeout:
        return {"success": False, "message": "⏱️ Backend timeout - try again in a moment"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def verify_otp_request(email, otp):
    """Verify OTP and get session token"""
    try:
        response = requests.post(
            f"{API_URL}/auth/verify-otp",
            json={"email": email, "otp": otp},
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "success": True,
                    "session_token": data.get("session_token"),
                    "email": data.get("email"),
                    "message": "OTP verified successfully"
                }
            else:
                return {"success": False, "message": data.get("message", "Invalid or expired OTP")}
        else:
            return {"success": False, "message": f"Server error: {response.status_code}"}
    
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Backend unavailable - use demo mode if OTP matches
        if hasattr(st.session_state, 'demo_otp') and st.session_state.demo_otp == otp:
            import uuid
            token = str(uuid.uuid4())
            return {
                "success": True,
                "session_token": token,
                "email": email,
                "message": "Demo Mode: Logged in (session data stored locally)"
            }
        else:
            return {"success": False, "message": "Invalid OTP or backend unreachable"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


# ============================================================================
# Session State & Initialization
# ============================================================================
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "session_token" not in st.session_state:
        st.session_state.session_token = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "login_step" not in st.session_state:
        st.session_state.login_step = "email"  # email or otp


def render_login_page():
    """Render the login page"""
    
    st.set_page_config(
        page_title="Login - IntelligentInsightAnalyzer",
        page_icon="🔐",
        layout="centered"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .login-container {
            max-width: 450px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .auth-header h1 {
            color: #1f77b4;
            margin-bottom: 0.5rem;
        }
        
        .step-indicator {
            display: flex;
            justify-content: space-around;
            margin-bottom: 2rem;
            gap: 1rem;
        }
        
        .step {
            text-align: center;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            background-color: #f0f0f0;
            flex: 1;
        }
        
        .step.active {
            background-color: #1f77b4;
            color: white;
        }
        
        .info-box {
            background-color: #f0f8ff;
            border-left: 4px solid #1f77b4;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0.25rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔐 IntelligentInsightAnalyzer")
    st.caption("Secure email-based authentication with OTP")
    
    st.divider()
    
    # Step 1: Email Input
    if st.session_state.login_step == "email":
        st.markdown("### Step 1: Enter Your Email")
        
        email = st.text_input(
            "Email Address",
            placeholder="your@email.com",
            key="email_input"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Send OTP", use_container_width=True):
                if not email or "@" not in email:
                    st.error("❌ Please enter a valid email address")
                else:
                    with st.spinner("🔄 Sending OTP..."):
                        result = send_otp_request(email)
                        
                        if result.get("success"):
                            st.session_state.user_email = email
                            st.session_state.login_step = "otp"
                            st.success(f"✅ {result['message']}")
                            st.info(f"💡 OTP valid for {OTP_VALID_MINUTES} minutes")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result['message'])
                            if result.get('details'):
                                st.code(result['details'])
        
        with col2:
            if st.button("📚 How it works?", use_container_width=True):
                st.info("""
                1. Enter your email
                2. We'll send you a 6-digit OTP
                3. Enter the OTP to login
                4. Your session lasts 24 hours
                """)
    
    # Step 2: OTP Verification
    elif st.session_state.login_step == "otp":
        st.markdown(f"### Step 2: Enter OTP")
        st.info(f"OTP sent to: **{st.session_state.user_email}**")
        
        otp = st.text_input(
            "Enter 6-digit OTP",
            placeholder="000000",
            max_chars=6,
            key="otp_input"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Verify OTP", use_container_width=True):
                if not otp or len(otp) != 6:
                    st.error("❌ Please enter a 6-digit OTP")
                else:
                    with st.spinner("🔄 Verifying OTP..."):
                        result = verify_otp_request(st.session_state.user_email, otp)
                        
                        if result.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.session_token = result['session_token']
                            st.session_state.user_email = result['email']
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(result['message'])
        
        with col2:
            if st.button("← Back", use_container_width=True):
                st.session_state.login_step = "email"
                st.session_state.user_email = None
                st.rerun()


def render_authenticated_page():
    """Render page for authenticated users"""
    
    st.set_page_config(
        page_title="Dashboard",
        page_icon="🏠",
        layout="wide"
    )
    
    # Sidebar profile with enhanced design
    with st.sidebar:
        st.divider()
        
        # Profile section with better styling
        email = st.session_state.user_email
        first_letter = email[0].upper() if email else "?"
        
        col1, col2 = st.columns([0.8, 2])
        with col1:
            st.markdown(f"""
            <div style="
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 20px;
                box-shadow: 0 2px 8px rgba(31, 119, 180, 0.3);
            ">
                {first_letter}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div>
                <p style="margin: 0; font-weight: bold; color: #1f77b4;">{email}</p>
                <p style="margin: 0; font-size: 12px; color: #666;">✅ Authenticated</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Logout button with better styling
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚪 Logout", use_container_width=True, help="End your session"):
                with st.spinner("Logging out..."):
                    try:
                        requests.post(
                            f"{API_URL}/auth/logout",
                            json={"session_token": st.session_state.session_token},
                            timeout=API_TIMEOUT
                        )
                    except:
                        pass  # Ignore errors during logout
                    
                    st.session_state.authenticated = False
                    st.session_state.session_token = None
                    st.session_state.user_email = None
                    st.success("✅ Logged out!")
                    time.sleep(1)
                    st.rerun()
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True, help="Refresh session"):
                st.rerun()
        
        st.divider()
        
        # Session info
        st.caption("📋 Session Information")
        st.info(f"""
        **Email:** {email}
        **Status:** Active ✅
        **Valid for:** 24 hours
        """)
    
    # Main content
    st.title("🏠 Welcome to IntelligentInsightAnalyzer")
    st.write(f"Hello, **{email}**! 👋")
    
    st.success("""
    ✅ **You are now authenticated!** 
    
    Your session is active and secure. You can now:
    """)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Data Analysis
        - Upload CSV/Excel files
        - Explore datasets
        - View statistics
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI Chat
        - Ask questions about data
        - Get insights
        - Multi-turn conversations
        """)
    
    with col3:
        st.markdown("""
        ### 📈 Advanced Features
        - Custom charts
        - Data quality checks
        - Temporal analytics
        """)
    
    st.info("""
    👈 **Next Steps:**
    1. Go back to the main app page
    2. Upload a CSV or Excel file from the sidebar
    3. Use the AI Chat tab to analyze your data
    """)


def main():
    """Main function"""
    init_session_state()
    
    # Check authentication status
    if st.session_state.authenticated:
        render_authenticated_page()
    else:
        render_login_page()


if __name__ == "__main__":
    main()
