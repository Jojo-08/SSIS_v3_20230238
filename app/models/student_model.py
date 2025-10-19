import re
from app.database import get_db

class Student:
     
    ID_PATTERN = re.compile(r'^\d{4}-\d{4}$')

    def __init__(self, student_id, first_name, last_name, program_code, year, gender ):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.program_code = program_code
        self.year = year
        self.gender = gender

        if not self.ID_PATTERN.match(self.student_id):
            raise ValueError("student id must be in YYYY-NNNN")

  

    def get_all(page=1,per_page=20):
        conn = get_db()
        cur = conn.cursor()
        offset = (page - 1) * per_page
        cur.execute("SELECT * FROM students ORDER by student_id LIMIT %s OFFSET %s",(per_page, offset))
        students = cur.fetchall()
        cur.close()
        return students

    def get_total_num():
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
        student = cur.fetchone()
        cur.close()
        return student

    def add_student(self):
        
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO students (student_id, first_name, last_name, program_code, year, gender) 
                        VALUES(%s,%s,%s,%s,%s,%s)""",
                        (self.student_id, self.first_name, self.last_name, self.program_code, self.year, self.gender))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(f"Error adding student: {e}")
            return False, f"Error adding student: {e}"
        finally:
            cur.close()

    def edit_student(self):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE students 
                        SET first_name = %s, last_name = %s, program_code = %s, year = %s, gender = %s 
                        WHERE student_id = %s""",
                        (self.first_name,self.last_name,self.program_code,self.year,self.gender,self.student_id))
            
            if cur.rowcount == 0:
                conn.commit()
                print(f"No student was found with ID = {self.student_id}")
                return False, f"No student was found with ID = {self.student_id}"
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