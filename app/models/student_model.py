import re
from app.database import get_db

class Student:
     
    ID_PATTERN = re.compile(r'^\d{4}-\d{4}$')

    def __init__(self, student_id, first_name, last_name, program_code, year, gender, photo_url=None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.program_code = program_code
        self.year = year
        self.gender = gender
        self.photo_url = photo_url

        if not self.ID_PATTERN.match(self.student_id):
            raise ValueError("student id must be in YYYY-NNNN")

  

    def get_all(page=1, per_page=20, sort_by='student_id', sort_order='asc'):
        conn = get_db()
        cur = conn.cursor()
        offset = (page - 1) * per_page
        
        # Whitelist allowed columns to prevent SQL injection
        allowed_columns = ['student_id', 'firstname', 'lastname', 'program_code', 'year', 'gender']
        if sort_by not in allowed_columns:
            sort_by = 'student_id'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'
        
        query = f"SELECT * FROM students ORDER BY {sort_by} {sort_order.upper()} LIMIT %s OFFSET %s"
        cur.execute(query, (per_page, offset))
        students = cur.fetchall()
        cur.close()
        return students

    def get_total_num():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM students")
        total = cur.fetchone()['count']
        cur.close()
        return total

    def get_student(student_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cur.fetchone()
        cur.close()
        return student

    def add_student(self):
        
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO students (student_id, firstname, lastname, program_code, year, gender, photo_url) 
                        VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                        (self.student_id, self.first_name, self.last_name, self.program_code, self.year, self.gender, self.photo_url))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(f"Error adding student: {e}")
            return False
        finally:
            cur.close()

    def edit_student(self):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE students 
                        SET firstname = %s, lastname = %s, program_code = %s, year = %s, gender = %s, photo_url = %s 
                        WHERE student_id = %s""",
                        (self.first_name,self.last_name,self.program_code,self.year,self.gender,self.photo_url,self.student_id))
            
            if cur.rowcount == 0:
                conn.commit()
                print(f"No student was found with ID = {self.student_id}")
                return False, f"No student was found with ID = {self.student_id}"
            conn.commit()
            return True, "Student updated successfully"
        
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
            cur.execute("DELETE FROM students WHERE student_id = %s",(student_id,))
            if cur.rowcount == 0:
                conn.commit()
                print(f"No student was found with ID = {student_id}")
                return False, f"No student was found with ID = {student_id}"
            conn.commit()
            return True, "Student deleted successfully"
        except Exception as e:
            conn.rollback()
            print(f"Error deleting student: {e}")
            return False, f"Error deleting student: {e}"
        finally:
            cur.close()