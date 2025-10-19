from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class StudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(),Regexp(r'^\d{4}-\d{4}$',message='Must be in YYYY-NNNN')])
    first_name = StringField('First Name', validators=[DataRequired(),Length(max=255,message='Your input has exceedded that maximum number of characters needed')])
    last_name = StringField('Last Name', validators=[DataRequired(),Length(max=255,message='Your input has exceedded that maximum number of characters needed')])
    program_code = SelectField('Program Code',
                    choices=[], validators=[DataRequired()])
    year = SelectField('Year', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProgramForm(FlaskForm):
    program_code = StringField('Program Code', validators=[DataRequired(),Length(max=10,message='Your input has exceedded that maximum number of characters needed')])
    program_name = StringField('Program Name', validators=[DataRequired(),Length(max=255,message='Your input has exceedded that maximum number of characters needed')])
    college_code = SelectField('College Code',
                    choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProgramForm(FlaskForm):
    college_code = StringField('College Code', validators=[DataRequired(),Length(max=10,message='Your input has exceedded that maximum number of characters needed')])
    college_name = StringField('College Name', validators=[DataRequired(),Length(max=255,message='Your input has exceedded that maximum number of characters needed')])
    submit = SubmitField('Submit')
