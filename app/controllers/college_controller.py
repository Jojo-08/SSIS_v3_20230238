from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models.college_model import College
from . import college_bp
from app.forms import CollegeForm

@college_bp.route('/')
@login_required
def list_colleges():
    page = request.args.get('page',1, type=int)
    per_page = 20
    colleges = College.get_all(page, per_page)
    total = College.get_total_num()

    add_form = CollegeForm()

    edit_forms = []
    for c in colleges:
        form = CollegeForm(
            college_code=c['college_code'],
            college_name=c['college_name']
        )
        edit_forms.append(form)
    
    open_modal = request.args.get('open_modal')

    college_forms = list(zip(colleges, edit_forms))
   
    return render_template('college/college.html', colleges=colleges, Total=total, page=page, add_form=add_form, college_forms=college_forms, open_modal=open_modal)

@college_bp.route('/add', methods=['POST'])
@login_required
def add():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    form = CollegeForm()
    
    if form.validate():
        college_code = form.college_code.data
        college_name = form.college_name.data

        try:
            new_college = College(college_code, college_name)
            success = new_college.add_college()
            if success:
                if is_ajax:
                    return jsonify({'success': True, 'message': 'College added successfully!'})
                flash("College added Successfully!", "success")
                return redirect(url_for('College.list_colleges'))
            else:
                if is_ajax:
                    return jsonify({'success': False, 'error': 'Failed to add college. College code may already exist.'}), 400
                flash("Failed to add college.", "danger")
        
        except ValueError as ve:
            if is_ajax:
                return jsonify({'success': False, 'error': str(ve)}), 400
            flash(str(ve),"danger")
        except Exception as e:
            if is_ajax:
                return jsonify({'success': False, 'error': str(e)}), 400
            flash(f"Error {e}","danger")
    else:
        errors = {field: errors for field, errors in form.errors.items()}
        if is_ajax:
            return jsonify({'success': False, 'errors': errors, 'error': 'Validation failed. Please check your input.'}), 400
    
    flash("Please fix the errors below.", "danger")
    return redirect(url_for('College.list_colleges', open_modal='addCollegeModal'))

@college_bp.route('/edit/<college_code>', methods=['POST'])
@login_required
def edit_college(college_code):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    form = CollegeForm(request.form)
    record = College.get_college(college_code)

    if not record:
        if is_ajax:
            return jsonify({'success': False, 'error': 'College not found!'}), 404
        flash('College not found!', 'danger')
        return redirect(url_for('College.list_colleges'))
    
    if form.validate():
        # Create college with new values from form
        c = College(form.college_code.data, form.college_name.data)
        
        try:
            # Pass the old college_code to identify which record to update
            success, message = c.edit_college(college_code)

            if success:
                if is_ajax:
                    return jsonify({'success': True, 'message': message})
                flash(message, "success")
            else:
                if is_ajax:
                    return jsonify({'success': False, 'error': message}), 400
                flash(message, "danger")

        except Exception as e:
            if is_ajax:
                return jsonify({'success': False, 'error': str(e)}), 400
            flash(f"Error: {e}", "danger")
            
        return redirect(url_for('College.list_colleges'))
    
    # Validation errors
    errors = {field: errors for field, errors in form.errors.items()}
    if is_ajax:
        return jsonify({'success': False, 'errors': errors, 'error': 'Validation failed. Please check your input.'}), 400
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")
    return redirect(url_for('College.list_colleges', open_modal=f'editCollegeModal-{college_code}'))

@college_bp.route('/delete/<college_code>', methods=['POST'])
@login_required
def delete_college(college_code):
    success, message = College.delete_college(college_code)

    if success:
        flash("College deleted successfully!", "success")
    else: 
        flash(message, "danger")
    
    return redirect(url_for('College.list_colleges'))