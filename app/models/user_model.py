from app.database import get_db
from flask_login import UserMixin
import hashlib

class User(UserMixin):

    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    def add_user(self):
        conn = get_db()
        cur = conn.cursor()

        password_hash = hashlib.md5(self.password.encode()).hexdigest()
        try:
            cur.execute ("INSERT INTO users(username, user_password) VALUES (%s, %s,%s)",
                     (self.username, password_hash, self.email))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding user: {e}")
            return False, f"Error adding user:{e}" 
        finally:
            cur.close()
    
    def check_password(self, password):
        password_hash = hashlib.md5(password.encode()).hexdigest()
        return self.password == password_hash
    
    def get(username):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = %s",(username))
            u = cur.fetchone()
            if u:
                user = User(id=u[0],username=u[1],password=u[2])
                return user
            else:
                return None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cur.close()
            
        