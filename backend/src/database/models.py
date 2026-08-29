"""
Database models for authentication
"""

from datetime import datetime, timedelta
import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'auth.db')


class Database:
    """SQLite database handler for authentication"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # OTPs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS otps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                otp_code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_used BOOLEAN DEFAULT 0,
                used_at TIMESTAMP
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, email: str) -> dict:
        """Create or get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (email) VALUES (?)',
                (email,)
            )
            conn.commit()
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # User already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            user_id = row['id']
        
        conn.close()
        return {'id': user_id, 'email': email}
    
    def save_otp(self, email: str, otp_code: str, validity_minutes: int = 5) -> bool:
        """Save OTP to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        expires_at = datetime.utcnow() + timedelta(minutes=validity_minutes)
        
        cursor.execute('''
            INSERT INTO otps (email, otp_code, expires_at)
            VALUES (?, ?, ?)
        ''', (email, otp_code, expires_at))
        
        conn.commit()
        conn.close()
        return True
    
    def verify_otp(self, email: str, otp_code: str) -> bool:
        """Verify OTP"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM otps 
            WHERE email = ? AND otp_code = ? AND is_used = 0
            ORDER BY created_at DESC LIMIT 1
        ''', (email, otp_code))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        # Check if OTP is expired
        expires_at = datetime.fromisoformat(row['expires_at'])
        if datetime.utcnow() > expires_at:
            conn.close()
            return False
        
        # Mark OTP as used
        cursor.execute('''
            UPDATE otps SET is_used = 1, used_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (row['id'],))
        
        # Update last login
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP
            WHERE email = ?
        ''', (email,))
        
        conn.commit()
        conn.close()
        return True
    
    def create_session(self, email: str, session_token: str, validity_hours: int = 24) -> bool:
        """Create session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        expires_at = datetime.utcnow() + timedelta(hours=validity_hours)
        
        cursor.execute('''
            INSERT INTO sessions (email, session_token, expires_at)
            VALUES (?, ?, ?)
        ''', (email, session_token, expires_at))
        
        conn.commit()
        conn.close()
        return True
    
    def verify_session(self, session_token: str) -> dict:
        """Verify session token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions 
            WHERE session_token = ? AND is_active = 1
        ''', (session_token,))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Check if session is expired
        expires_at = datetime.fromisoformat(row['expires_at'])
        if datetime.utcnow() > expires_at:
            conn.close()
            return None
        
        conn.close()
        return {'email': row['email']}
    
    def invalidate_session(self, session_token: str) -> bool:
        """Invalidate session (logout)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions SET is_active = 0
            WHERE session_token = ?
        ''', (session_token,))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user(self, email: str) -> dict:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'email': row['email'],
                'created_at': row['created_at'],
                'last_login': row['last_login']
            }
        return None


# Global database instance
db = Database()
