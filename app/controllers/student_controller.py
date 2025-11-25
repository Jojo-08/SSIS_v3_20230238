import os
import io
from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models.student_model import Student
from app.models.program_model import Program
from . import student_bp
from app.forms import StudentForm
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "SSISV3"

def upload_resized_image(photo, student_id):
    """
    Resizes image to max 300x300, preserves PNG/JPEG format, and uploads to Supabase.
    """
    # 1. Open the image using Pillow
    img = Image.open(photo)
    
    # 2. Determine the format (default to JPEG if unknown)
    # img.format returns 'JPEG', 'PNG', 'GIF', etc.
    original_format = img.format if img.format in ['JPEG', 'PNG'] else 'JPEG'
    
    # 3. Handle Colorspace 
    # If saving as JPEG, we must convert RGBA (Transparency) to RGB
    if original_format == 'JPEG' and img.mode != 'RGB':
        img = img.convert('RGB')
    # If PNG, we keep RGBA to preserve transparency
        
    # 4. Resize (Thumbnail limits max dimension to 300px)
    img.thumbnail((300, 300))
    
    # 5. Save to a memory buffer
    buffer = io.BytesIO()
    
    # 'optimize=True' helps reduce size for both PNG and JPEG without losing quality
    img.save(buffer, format=original_format, optimize=True, quality=85)
    buffer.seek(0)
    
    # 6. Set Content Type based on format
    mime_type = "image/png" if original_format == 'PNG' else "image/jpeg"
    
    # 7. Define Path
    # We use the original filename to keep the correct extension (.png or .jpg)
    # We use secure_filename to clean up spaces/weird characters (optional but recommended)
    from werkzeug.utils import secure_filename
    clean_filename = secure_filename(photo.filename)
    file_path = f"student_photos/{student_id}_{clean_filename}"

    # 8. Upload to Supabase
    supabase.storage.from_(BUCKET_NAME).upload(
        file_path, 
        buffer.read(), 
        {"content-type": mime_type, "upsert": "true"}
    )
    
    return file_path

@student_bp.route('/')
@login_required
def list_students():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    students = Student.get_all(page, per_page)
    total = Student.get_total_num()

    # Generate signed URLs for private access
    for s in students:
        if s['photo_url']:
            # If it's a full URL (legacy), try to extract path or just use it if it works
            # But for private buckets, we need signed URLs.
            # We assume s['photo_url'] contains the file path (e.g. "student_photos/...")
            # If it contains a full URL, we might need to parse it.
            path = s['photo_url']
            if path.startswith('http'):
                # Try to extract the path after the bucket name
                # URL format: .../storage/v1/object/public/BUCKET_NAME/path/to/file
                if f"/{BUCKET_NAME}/" in path:
                    path = path.split(f"/{BUCKET_NAME}/")[-1]
            
            try:
                # Create a signed URL valid for 1 hour (3600 seconds)
                res = supabase.storage.from_(BUCKET_NAME).create_signed_url(path, 3600)
                if res and 'signedURL' in res:
                    s['photo_url'] = res['signedURL']
            except Exception as e:
                print(f"Error signing URL for {s['student_id']}: {e}")

    # Get all programs for the dropdown
    all_programs = Program.get_all(page=1, per_page=100)
    program_choices = [(p['program_code'], p['program_code']) for p in all_programs]
    
    add_form = StudentForm()
    add_form.program_code.choices = program_choices

    edit_forms = []
    for s in students:
        form = StudentForm(
            student_id=s['student_id'],
            first_name=s['firstname'],
            last_name=s['lastname'],
            program_code=s['program_code'],
            year=s['year'],
            gender=s['gender']
        )
        form.program_code.choices = program_choices
        edit_forms.append(form)
    
    open_modal =request.args.get('open_modal')

    student_forms = list(zip(students,edit_forms))
    return render_template('student/student.html', Total=total, page=page, add_form=add_form, student_forms=student_forms, students=students, open_modal=open_modal)

@student_bp.route('/add', methods=['POST'])
@login_required
def add():
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Populate program choices for validation
    all_programs = Program.get_all(page=1, per_page=100)
    program_choices = [(p['program_code'], p['program_code']) for p in all_programs]
    
    form = StudentForm()
    form.program_code.choices = program_choices
    
    if form.validate():
        student_id = form.student_id.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        program_code = form.program_code.data
        year = form.year.data
        gender = form.gender.data
        
        photo = request.files.get('photo')
        photo_url = None

        if photo and photo.filename:
            try:
                print(f"Processing and uploading photo for {student_id}...")
                
                # CALL THE upload_resized_image() FUNCTION HERE
                photo_url = upload_resized_image(photo, student_id)
                
                print(f"Upload successful. Path: {photo_url}")
            except Exception as e:
                print(f"Error uploading photo: {e}")
                if is_ajax:
                    return jsonify({'success': False, 'error': f"Error uploading photo: {e}"}), 400
                flash(f"Error uploading photo: {e}", "danger")

        try:
            new_student = Student(student_id, first_name, last_name, 
                                  program_code, year, gender, photo_url)
            success = new_student.add_student()

            if success:
                if is_ajax:
                    return jsonify({'success': True, 'message': 'Student added successfully!'})
                flash("Student added Successfully!", "success")
                return redirect(url_for('Student.list_students'))
            else:
                if is_ajax:
                    return jsonify({'success': False, 'error': 'Failed to add student. Student ID may already exist.'}), 400
                flash("Failed to add student.", "danger")
        
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
    return redirect(url_for('Student.list_students', open_modal='addStudentModal'))

@student_bp.route('/edit/<student_id>', methods=['POST'])
@login_required
def edit_student(student_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Initialize form without arguments to automatically handle request.form and request.files
    form = StudentForm()
    
    # Populate program choices for validation
    all_programs = Program.get_all(page=1, per_page=100)
    form.program_code.choices = [(p['program_code'], p['program_code']) for p in all_programs]
    
    record = Student.get_student(student_id)

    if not record:
        if is_ajax:
            return jsonify({'success': False, 'error': 'Student not found!'}), 404
        flash('Student not found!', 'danger')
        return redirect(url_for('Student.list_students'))
    
    if form.validate():
        
        photo = request.files.get('photo')
        photo_url = record['photo_url'] # Default to existing

        if photo and photo.filename:
            try:
                print(f"Processing and uploading photo for {student_id}...")
                
                # CALL THE upload_resized_image() FUNCTION HERE
                # This will return the new path to update the database with
                photo_url = upload_resized_image(photo, student_id)
                
                print(f"Upload successful. Path: {photo_url}")
            except Exception as e:
                print(f"Error uploading photo: {e}")
                if is_ajax:
                    return jsonify({'success': False, 'error': f"Error uploading photo: {e}"}), 400
                flash(f"Error uploading photo: {e}", "danger")

        # If no new photo uploaded, keep the existing one
        if not photo_url:
            # because photo_url is already set to record['photo_url'] above
            pass

        s = Student(student_id, 
                    form.first_name.data, 
                    form.last_name.data, 
                    form.program_code.data, 
                    form.year.data, 
                    form.gender.data,
                    photo_url)
                 
        try:
            success, message = s.edit_student()

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
            
        return redirect(url_for('Student.list_students'))
    
    # Validation errors
    errors = {field: errors for field, errors in form.errors.items()}
    if is_ajax:
        return jsonify({'success': False, 'errors': errors, 'error': 'Validation failed. Please check your input.'}), 400
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")
    return redirect(url_for('Student.list_students', open_modal=f'editStudentModal-{student_id}'))

@student_bp.route('/delete/<student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    success, message = Student.delete_student(student_id)

    if success:
        flash("Student deleted successfully!", "success")
    else: 
        flash(message, "danger")
    
    return redirect(url_for('Student.list_students'))