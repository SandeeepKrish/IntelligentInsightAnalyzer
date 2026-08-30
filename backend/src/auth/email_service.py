import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    def __init__(self):
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        self.use_mock = not (self.gmail_user and self.gmail_password)
    
    def generate_otp(self, length=6):
        return ''.join(random.choices("0123456789", k=length))
    
    def send_otp_email(self, email, otp_code):
        if self.use_mock:
            print(f"\n{'='*60}")
            print(f"MOCK MODE - OTP for {email}: {otp_code}")
            print(f"{'='*60}\n")
            return True
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = email
            msg['Subject'] = 'Your IntelligentInsightAnalyzer OTP'
            
            body = f"""Hello,

Your One-Time Password (OTP) for IntelligentInsightAnalyzer is:

{otp_code}

This OTP is valid for 5 minutes.

Best regards,
IntelligentInsightAnalyzer Team"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            print(f"Attempting to send email to {email}...")
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email sent successfully to {email}")
            return True
        
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False


email_service = EmailService()
