from app.database import get_db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def __init__(self, id=None, username=None, email=None, password=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def add_user(self):
        conn = get_db()
        cur = conn.cursor()

        password_hash = generate_password_hash(self.password)
        try:
            cur.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
                     (self.username, self.email, password_hash))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding user: {e}")
            return False
        finally:
            cur.close()
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def get(username):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            u = cur.fetchone()
            if u:
                user = User(id=u['user_id'], username=u['username'], email=u['email'], password=u['password'])
                return user
            else:
                return None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cur.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            u = cur.fetchone()
            if u:
                user = User(id=u['user_id'], username=u['username'], email=u['email'], password=u['password'])
                return user
            else:
                return None
        except Exception as e:
            print(f"Error fetching user by id: {e}")
            return None
        finally:
            cur.close()
            
        