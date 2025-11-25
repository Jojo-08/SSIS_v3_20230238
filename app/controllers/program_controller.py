from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models.program_model import Program
from app.models.college_model import College
from . import program_bp
from app.forms import ProgramForm


@program_bp.route('/')
@login_required
def list_programs():
    page = request.args.get('page',1, type=int)
    per_page = 20
    programs = Program.get_all(page, per_page)
    total = Program.get_total_num()

    # Get all colleges for the dropdown
    all_colleges = College.get_all(page=1, per_page=100)
    college_choices = [(c['college_code'], c['college_code']) for c in all_colleges]

    add_form = ProgramForm()
    add_form.college_code.choices = college_choices

    edit_forms = []
    for p in programs:
        form = ProgramForm(
            program_code=p['program_code'],
            program_name=p['program_name'],
            college_code=p['college_code']
        )
        form.college_code.choices = college_choices
        edit_forms.append(form)
    
    open_modal = request.args.get('open_modal')

    program_forms = list(zip(programs, edit_forms))
   
    return render_template('program/program.html', programs=programs, Total=total, page=page, add_form=add_form, program_forms=program_forms, open_modal=open_modal)

@program_bp.route('/add', methods=['POST'])
def add():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Populate college choices for validation
    all_colleges = College.get_all(page=1, per_page=100)
    college_choices = [(c['college_code'], c['college_code']) for c in all_colleges]
    
    form = ProgramForm()
    form.college_code.choices = college_choices
    
    if form.validate():
        program_code = form.program_code.data
        program_name = form.program_name.data
        college_code = form.college_code.data

        try:
            new_program = Program(program_code, program_name, college_code)
            success = new_program.add_program()
            if success:
                if is_ajax:
                    return jsonify({'success': True, 'message': 'Program added successfully!'})
                flash("Program added Successfully!", "success")
                return redirect(url_for('Program.list_programs'))
            else:
                if is_ajax:
                    return jsonify({'success': False, 'error': 'Failed to add program. Program code may already exist.'}), 400
                flash("Failed to add program.", "danger")
        
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
    return redirect(url_for('Program.list_programs', open_modal='addProgramModal'))

@program_bp.route('/edit/<program_code>', methods=['POST'])
def edit_program(program_code):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    form = ProgramForm(request.form)
    
    # Populate college choices for validation
    all_colleges = College.get_all(page=1, per_page=100)
    form.college_code.choices = [(c['college_code'], c['college_code']) for c in all_colleges]
    
    record = Program.get_program(program_code)

    if not record:
        if is_ajax:
            return jsonify({'success': False, 'error': 'Program not found!'}), 404
        flash('Program not found!', 'danger')
        return redirect(url_for('Program.list_programs'))
    
    if form.validate():
        # Create program with new values from form
        p = Program(form.program_code.data, form.program_name.data, form.college_code.data)
        
        try:
            # Pass the old program_code to identify which record to update
            success, message = p.edit_program(program_code)

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
            
        return redirect(url_for('Program.list_programs'))
    
    # Validation errors
    errors = {field: errors for field, errors in form.errors.items()}
    if is_ajax:
        return jsonify({'success': False, 'errors': errors, 'error': 'Validation failed. Please check your input.'}), 400
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")
    return redirect(url_for('Program.list_programs', open_modal=f'editProgramModal-{program_code}'))

@program_bp.route('/delete/<program_code>', methods=['POST'])
def delete_program(program_code):
    success, message = Program.delete_program(program_code)

    if success:
        flash("Program deleted successfully!", "success")
    else: 
        flash(message, "danger")
    
    return redirect(url_for('Program.list_programs'))