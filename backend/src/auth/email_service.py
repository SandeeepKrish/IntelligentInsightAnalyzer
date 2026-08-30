import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
    
    def generate_otp(self, length=6):
        return ''.join(random.choices('0123456789', k=length))
    
    def send_otp_email(self, email, otp_code):
        if self.use_mock:
            print(f"\n{'='*60}")
            print(f"📧 MOCK EMAIL (Testing Mode)")
            print(f"To: {email}")
            print(f"OTP Code: {otp_code}")
            print(f"Valid for: 5 minutes")
            print(f"{'='*60}\n")
            return True
        
        if not self.gmail_user or not self.gmail_password:
            print("Gmail credentials not configured. Using mock mode.")
            return True
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = email
            msg['Subject'] = 'Your IntelligentInsightAnalyzer OTP'
            
            body = f"Your OTP: {otp_code}\nValid for 5 minutes."
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False


email_service = EmailService(use_mock=True)
