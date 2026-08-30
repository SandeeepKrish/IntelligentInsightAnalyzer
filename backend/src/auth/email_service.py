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
        
        if self.use_mock:
            print("\n" + "="*60)
            print("⚠️  EMAIL SERVICE: Running in MOCK MODE")
            print("Gmail credentials not found. Set GMAIL_USER and GMAIL_APP_PASSWORD")
            print("="*60 + "\n")
        else:
            print("\n" + "="*60)
            print("✅ EMAIL SERVICE: Real SMTP enabled")
            print(f"   Using: {self.gmail_user}")
            print("="*60 + "\n")
    
    def generate_otp(self, length=6):
        """Generate random OTP"""
        return ''.join(random.choices("0123456789", k=length))
    
    def send_otp_email(self, email, otp_code):
        """Send OTP via email (real SMTP or mock mode)"""
        if self.use_mock:
            print(f"\n{'='*60}")
            print(f"📧 MOCK EMAIL: OTP for {email}")
            print(f"{'='*60}")
            print(f"🔐 OTP Code: {otp_code}")
            print(f"⏱️  Valid for: 5 minutes")
            print(f"{'='*60}\n")
            return True
        
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = email
            msg['Subject'] = '🔐 Your IntelligentInsightAnalyzer OTP'
            
            # Professional HTML body
            body = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
      <h2 style="color: #1f77b4;">IntelligentInsightAnalyzer</h2>
      
      <p>Hello,</p>
      
      <p>Your One-Time Password (OTP) for IntelligentInsightAnalyzer is:</p>
      
      <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
        <h1 style="color: #1f77b4; letter-spacing: 5px; font-family: monospace;">{otp_code}</h1>
      </div>
      
      <p><strong>⏱️ Valid for 5 minutes only</strong></p>
      
      <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
      
      <p style="font-size: 12px; color: #666;">
        If you did not request this OTP, please ignore this email.<br>
        Do not share this code with anyone.
      </p>
      
      <p style="margin-top: 30px; color: #666;">
        Best regards,<br>
        <strong>IntelligentInsightAnalyzer Team</strong>
      </p>
    </div>
  </body>
</html>
"""
            
            msg.attach(MIMEText(body, 'html'))
            
            print(f"📧 Sending OTP to {email}...")
            
            # Send via Gmail SMTP
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent successfully to {email}")
            return True
        
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Email Authentication Error: Invalid Gmail credentials")
            print(f"   Details: {str(e)}")
            return False
        
        except smtplib.SMTPException as e:
            print(f"❌ Email Send Error: {str(e)}")
            return False
        
        except Exception as e:
            print(f"❌ Unexpected Email Error: {str(e)}")
            return False


# Global instance
email_service = EmailService()
