import re
from . import program_model
from app.database import get_db, close_db

ID_PATTERN = re.compile(r'^\d{4}-\d{4}$')

def validate_id (student_id):
    if not ID_PATTERN.match(student_id):
        raise ValueError("student_id must be in YYYY-NNNN")

def get_all_students(page=1,per_page=20):
    conn = get_db()
    cur = conn.cursor()
    offset = (page - 1) * per_page
    cur.execute("SELECT * FROM students ORDER by student_id LIMIT %s OFFSET %s",(per_page, offset))
    rows = cur.fetchall()
    cur.close()
    return rows

def get_total_students():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM students")
    total = cur.fetchone()[0]
    cur.close()
    return total

def get_student(student_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id))
    s = cur.fetchone()
    cur.close()
    return s

def add_student(student_id, first_name, last_name, year, gender, program_code ):
    
    validate_id(student_id)
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO students (student_id, first_name, last_name, program_code, year, gender) 
                    VALUES(%s,%s,%s,%s,%s,%s)""",(student_id, first_name, last_name, program_code, year, gender))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error adding student: {e}")
        return False, f"Error adding student: {e}"
    finally:
        cur.close()

def edit_student(student_id,first_name,last_name,program_code, year, gender):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""UPDATE students 
                       SET first_name = %s, last_name = %s, program_code = %s, year = %s, gender = %s 
                       WHERE student_id = %s""",
                       (first_name,last_name,program_code,year,gender,student_id))
        
        if cur.rowcount == 0:
            conn.commit()
            print(f"No student was found with ID = {student_id}")
            return False, f"No student was found with ID = {student_id}"
        conn.commit()
        return True
    
    except Exception as e:
        conn.rollback()
        print(f"Error updating student: {e}")
        return False, f"Error updating student: {e}"
    finally:
        cur.close()

def delete_student(student_id):
    conn = get_db()
    cur = conn.cursor()
    try: 
        cur.execute("DELETE FROM students WHERE student_id = %s",(student_id))
        if cur.rowcount == 0:
            conn.commit()
            print(f"No student was found with ID = {student_id}")
            return False, f"No student was found with ID = {student_id}"
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error deleting student: {e}")
        return False, f"Error deleting student: {e}"
    finally:
        cur.close()