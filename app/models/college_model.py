import re
from app.database import get_db

class College:
     
    def __init__(self, college_code, college_name):
        self.college_code = college_code
        self.college_name = college_name
        
        
  

    def get_all(page=1,per_page=20):
        conn = get_db()
        cur = conn.cursor()
        offset = (page - 1) * per_page
        cur.execute("SELECT * FROM colleges ORDER by college_code LIMIT %s OFFSET %s",(per_page, offset))
        colleges = cur.fetchall()
        cur.close()
        return colleges

    def get_total_num():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM colleges")
        total = cur.fetchone()[0]
        cur.close()
        return total

    def get_college(college_code):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM colleges WHERE college_code = %s", (college_code))
        college = cur.fetchone()
        cur.close()
        return college

    def add_college(self):
        
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO colleges (college_code, college_name) 
                        VALUES(%s,%s)""",
                        (self.college_code, self.college_name))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(f"Error adding college: {e}")
            return False, f"Error adding college: {e}"
        finally:
            cur.close()

    def edit_college(self,college_code):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE colleges 
                        SET college_code = %s, college_name = %s
                        WHERE college_code = %s""",
                        (college_code,self.college_name,self.college_code))
            
            if cur.rowcount == 0:
                conn.commit()
                print(f"No college was found with code = {self.college_code}")
                return False, f"No college was found with code = {self.college_code}"
            conn.commit()
            return True
        
        except Exception as e:
            conn.rollback()
            print(f"Error updating college: {e}")
            return False, f"Error updating college: {e}"
        finally:
            cur.close()

    def delete_college(college_code):
        conn = get_db()
        cur = conn.cursor()
        try: 
            cur.execute("DELETE FROM colleges WHERE college_code = %s",(college_code))
            if cur.rowcount == 0:
                conn.commit()
                print(f"No college was found with code = {college_code}")
                return False, f"No college was found with code = {college_code}"
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error deleting college: {e}")
            return False, f"Error deleting college: {e}"
        finally:
            cur.close()