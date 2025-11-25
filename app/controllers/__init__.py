from flask import Blueprint

student_bp  = Blueprint('Student', __name__, url_prefix ='/students')
program_bp  = Blueprint('Program', __name__, url_prefix ='/programs')
college_bp  = Blueprint('College', __name__, url_prefix ='/colleges')
user_bp = Blueprint('User',__name__,url_prefix='/user')
main_bp = Blueprint('Main',__name__, url_prefix='/')
from . import college_controller, main_controller, program_controller, student_controller, user_controller