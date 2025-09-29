from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landing_screen():
    return "Default"

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/college/')
def colleges():
    return render_template("college.html")

@app.route('/program/')
def programs():
    return render_template("program.html") 

@app.route('/student/')
def students():
    return render_template("student.html") 

@app.route('/college/<collegeCode>')
def college(collegeCode):
    return 'college: %s' % collegeCode

@app.route('/student/<int:studentID>')
def student(studentID):
    return 'student :%d' % studentID

@app.route('/program/<programCode>')
def program(programCode):
    return 'program : %s' % programCode

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
