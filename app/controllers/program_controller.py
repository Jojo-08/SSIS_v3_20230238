from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.program_model import Program
from . import program_bp


@program_bp.route('/')
def list_programs():
    page = request.args.get('page',1, type=int)
    per_page = 20
    programs = Program.get_all(page, per_page)
    total = Program.get_total_num()
   
    return render_template('program.html', programs=programs, total=total, page=page)

@program_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        program_code = request.form['program_code']
        program_name = request.form['program_name']
        college_code = request.form['college_code']

        try:
            new_program = Program(program_code, program_name, college_code)
            success = new_program.add_program()
            if success:
                flash("Program added Successfully!", "success")
                return redirect(url_for('Program.list_programs'))
        
        except ValueError as ve:
            flash(str(ve),"danger")
        except Exception as e:
            flash(f"Error {e}","danger")
    
    return render_template('programs/add.html')

@program_bp.route('/edit/<program_code>', methods=['GET','POST'])
def edit_program(program_code):
    record = Program.get_program(program_code)

    if not record:
        flash('Program not found!', 'danger')
        return redirect(url_for('Program.list_programs'))
    
    if request.method == 'POST':
        program_code = request.form['program_code']
        program_name = request.form['program_name']
        college_code = request.form['college_code']

        p = Program(program_code, program_name, college_code)
        success = p.edit_program()

        if success:
            flash("Program updated successfully!", "success")
            return redirect(url_for('Program.list_programs'))
        else:
            flash("Update failed!", "danger")
    
    return render_template('programs/edit.html', Program=record)

@program_bp.route('/delete/<program_code>', methods=['POST'])
def delete_program(program_code):
    success, message = Program.delete_program(program_code)

    if success:
        flash("Program deleted successfully", "success")
    
    else: 
        flash( message, "danger")
    
    return redirect(url_for('Program.list_programs'))