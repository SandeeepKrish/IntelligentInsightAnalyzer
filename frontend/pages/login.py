"""
Login page for IntelligentInsightAnalyzer
"""

import streamlit as st
import requests
import time

# API endpoint (change to your server URL)
API_URL = "http://localhost:8000"

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


def render_login_page():
    """Render the login page"""
    
    st.set_page_config(
        page_title="Login - IntelligentInsightAnalyzer",
        page_icon="🔐",
        layout="centered"
    )
    
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔐 IntelligentInsightAnalyzer")
    st.caption("Login to continue with your analysis")
    
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
                    with st.spinner("Sending OTP..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/auth/send-otp",
                                json={"email": email},
                                timeout=10
                            )
                            
                            if response.status_code == 200:
                                st.session_state.user_email = email
                                st.session_state.login_step = "otp"
                                st.success("✅ OTP sent! Check your console or email.")
                                st.info("💡 In mock mode, OTP appears in console/terminal")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error(f"❌ Error: {response.json().get('detail', 'Failed to send OTP')}")
                        
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot connect to auth server. Make sure FastAPI is running on http://localhost:8000")
                            st.info("Run: `cd backend && python -m auth.auth_service`")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
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
                    with st.spinner("Verifying OTP..."):
                        try:
                            response = requests.post(
                                f"{API_URL}/auth/verify-otp",
                                json={
                                    "email": st.session_state.user_email,
                                    "otp": otp
                                },
                                timeout=10
                            )
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.session_state.authenticated = True
                                st.session_state.session_token = data['session_token']
                                st.session_state.user_email = data['email']
                                st.success("✅ Login successful!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Invalid or expired OTP")
                        
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot connect to auth server")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
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
    
    # Sidebar profile
    with st.sidebar:
        st.divider()
        
        # Profile badge
        email = st.session_state.user_email
        first_letter = email[0].upper() if email else "?"
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div style="
                width: 40px;
                height: 40px;
                background-color: #1f77b4;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 18px;
            ">
                {first_letter}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**{email}**")
            st.caption("Logged in")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            with st.spinner("Logging out..."):
                try:
                    requests.post(
                        f"{API_URL}/auth/logout",
                        json={"email": st.session_state.session_token},
                        timeout=10
                    )
                except:
                    pass
                
                st.session_state.authenticated = False
                st.session_state.session_token = None
                st.session_state.user_email = None
                st.success("✅ Logged out!")
                time.sleep(1)
                st.rerun()
        
        st.divider()
    
    # Main content
    st.title("🏠 Welcome to IntelligentInsightAnalyzer")
    st.write(f"Hello, **{email}**!")
    
    st.info("""
    ✅ You are now authenticated! 
    
    Go to the main app to:
    - Upload CSV/Excel files
    - Perform data analysis
    - Chat with AI about your data
    - View advanced analytics
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
