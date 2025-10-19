from flask import Flask
from config import SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    from app.database import init_app as init_db
    init_db(app)
    from app.controllers import user_bp, student_bp,program_bp,college_bp,main_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(college_bp)
    app.register_blueprint(main_bp)
    return app