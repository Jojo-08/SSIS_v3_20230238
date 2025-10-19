from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.student_model import Student
from . import student_bp

@student_bp.route('/')
def list_students():
    page = request.args.get('page',1, type=int)
    per_page = 20
    students = Student.get_all(page, per_page)
    total = Student.get_total_num()
   
    return render_template('student.html', students=students, total=total, page=page)

@student_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        program_code = request.form['program_code']
        year = request.form['year']
        gender = request.form['gender'] 

        try:
            new_student = Student(student_id, first_name, last_name, 
                                  program_code, year, gender)
            success = new_student.add_student()
            if success:
                flash("Student added Successfully!", "success")
                return redirect(url_for('Student.list_students'))
        
        except ValueError as ve:
            flash(str(ve),"danger")
        except Exception as e:
            flash(f"Error {e}","danger")
    
    return render_template('students/add.html')

@student_bp.route('/edit/<student_id>', methods=['GET','POST'])
def edit_student(student_id):
    record = Student.get_student(student_id)

    if not record:
        flash('Student not found!', 'danger')
        return redirect(url_for('Student.list_students'))
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        program_code = request.form['program_code']
        year = request.form['year']
        gender = request.form['gender']

        s = Student(student_id, first_name, last_name, 
                                  program_code, year, gender)
        success = s.edit_student()

        if success:
            flash("Student updated successfully!", "success")
            return redirect(url_for('Student.list_students'))
        else:
            flash("Update failed!", "danger")
    
    return render_template('students/edit.html', student=record)

@student_bp.route('/delete/<student_id>', methods=['POST'])
def delete_sudent(student_id):
    success, message = Student.delete_student(student_id)

    if success:
        flash("Student deleted successfully", "success")
    
    else: 
        flash( message, "danger")
    
    return redirect(url_for('Student.list_students'))