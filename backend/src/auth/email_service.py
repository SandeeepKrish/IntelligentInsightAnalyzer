"""
Email service for sending OTPs
"""

import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    """Email service for OTP delivery"""
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize email service
        
        Args:
            use_mock: If True, print OTP to console (for testing)
                     If False, use actual SMTP (requires Gmail app password)
        """
        self.use_mock = use_mock
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
    
    def generate_otp(self, length: int = 6) -> str:
        """Generate random OTP"""
        return ''.join(random.choices('0123456789', k=length))
    
    def send_otp_email(self, email: str, otp_code: str) -> bool:
        """Send OTP via email"""
        
        if self.use_mock:
            print(f"\n{'='*60}")
            print(f"📧 MOCK EMAIL (Testing Mode)")
            print(f"{'='*60}")
            print(f"To: {email}")
            print(f"Subject: Your IntelligentInsightAnalyzer OTP")
            print(f"\nOTP Code: {otp_code}")
            print(f"Valid for: 5 minutes")
            print(f"{'='*60}\n")
            return True
        
        # Real email sending
        if not self.gmail_user or not self.gmail_password:
            print("❌ Gmail credentials not configured. Using mock mode.")
            return self.send_otp_email_mock(email, otp_code)
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = email
            msg['Subject'] = 'Your IntelligentInsightAnalyzer OTP'
            
            # Email body
            body = f"""
            Hello,
            
            Your One-Time Password (OTP) for IntelligentInsightAnalyzer is:
            
            {otp_code}
            
            This OTP is valid for 5 minutes.
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            IntelligentInsightAnalyzer Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send via Gmail SMTP
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            return True
        
        except Exception as e:
            print(f"❌ Email sending failed: {str(e)}")
            return False
    
    def send_otp_email_mock(self, email: str, otp_code: str) -> bool:
        """Mock email sending for testing"""
        print(f"\n{'='*60}")
        print(f"📧 MOCK EMAIL (Testing Mode)")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Subject: Your IntelligentInsightAnalyzer OTP")
        print(f"\nOTP Code: {otp_code}")
        print(f"Valid for: 5 minutes")
        print(f"{'='*60}\n")
        return True


# Global email service instance (mock mode by default)
email_service = EmailService(use_mock=True)
