from flask import Flask
from flask_login import LoginManager, AnonymousUserMixin
from app.config import SECRET_KEY,DB_CONFIG
from dotenv import load_dotenv
import os

load_dotenv()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
    
    login_manager.init_app(app)
    login_manager.login_view = 'User.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
  
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user_model import User
        return User.get_by_id(user_id)
   
    from app.database import init_app as init_db
    init_db(app)

    from app.controllers import user_bp, student_bp,program_bp,college_bp,main_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(college_bp)
    app.register_blueprint(main_bp)

    print(app.url_map)
    print("flask app initiated successfully")
    return app