from flask import Flask
from config import SECRET_KEY
from app.database import init_app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    init_app(app)
    from app.controllers.user_controller import user_bp
    from app.controllers.student_controller import student_bp
    from app.controllers.program_controller import program_bp
    from app.controllers.college_controller import college_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(program_bp)
    app.register_blueprint(college_bp)
    
    return app