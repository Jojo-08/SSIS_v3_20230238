from flask import Flask

app = Flask(__name__)

@app.route('/')

def landing_screen():
    return "Default"

@app.route('/college/')
def college():
    return 'colleges' 
@app.route('/program/')
def college():
    return 'programs' 

@app.route('/student/')
def college():
    return 'students' 

@app.route('/college/<collegeCode>')
def college(collegeCode):
    return 'college: %s' % collegeCode

@app.route('/student/<int:studentID>')
def college(studentID):
    return 'student :%d' % studentID

@app.route('/program/<programCode>')
def college(programCode):
    return 'student : %s' % programCode

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
