from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.college_model import College
from . import college_bp

@college_bp.route('/')
def list_colleges():
    page = request.args.get('page',1, type=int)
    per_page = 20
    colleges = College.get_all(page, per_page)
    total = College.get_total_num()
   
    return render_template('college.html', colleges=colleges, total=total, page=page)

@college_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        try:
            new_college = College(college_code, college_name)
            success = new_college.add_college()
            if success:
                flash("College added Successfully!", "success")
                return redirect(url_for('College.list_colleges'))
        
        except ValueError as ve:
            flash(str(ve),"danger")
        except Exception as e:
            flash(f"Error {e}","danger")
    
    return render_template('colleges/add.html')

@college_bp.route('/edit/<college_code>', methods=['GET','POST'])
def edit_college(college_code):
    record = College.get_college(college_code)

    if not record:
        flash('College not found!', 'danger')
        return redirect(url_for('College.list_colleges'))
    
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        c = College(college_code, college_name)
        success = c.edit_college()

        if success:
            flash("College updated successfully!", "success")
            return redirect(url_for('College.list_colleges'))
        else:
            flash("Update failed!", "danger")
    
    return render_template('colleges/edit.html', College=record)

@college_bp.route('/delete/<college_code>', methods=['POST'])
def delete_college(college_code):
    success, message = College.delete_college(college_code)

    if success:
        flash("College deleted successfully", "success")
    
    else: 
        flash( message, "danger")
    
    return redirect(url_for('College.list_colleges'))