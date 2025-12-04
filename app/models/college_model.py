import re
from app.database import get_db

class College:
     
    def __init__(self, college_code, college_name):
        self.college_code = college_code
        self.college_name = college_name
        
        
  

    def get_all(page=1, per_page=20, sort_by='college_code', sort_order='asc'):
        conn = get_db()
        cur = conn.cursor()
        offset = (page - 1) * per_page
        
        # Whitelist allowed columns to prevent SQL injection
        allowed_columns = ['college_code', 'college_name']
        if sort_by not in allowed_columns:
            sort_by = 'college_code'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'
        
        query = f"SELECT * FROM colleges ORDER BY {sort_by} {sort_order.upper()} LIMIT %s OFFSET %s"
        cur.execute(query, (per_page, offset))
        colleges = cur.fetchall()
        cur.close()
        return colleges

    def get_total_num():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM colleges")
        total = cur.fetchone()['count']
        cur.close()
        return total

    def get_college(college_code):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM colleges WHERE college_code = %s", (college_code,))
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
            return False
        finally:
            cur.close()

    def edit_college(self, old_college_code):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE colleges 
                        SET college_code = %s, college_name = %s
                        WHERE college_code = %s""",
                        (self.college_code, self.college_name, old_college_code))
            
            if cur.rowcount == 0:
                conn.commit()
                print(f"No college was found with code = {old_college_code}")
                return False, f"No college was found with code: {old_college_code}"
            conn.commit()
            return True, "College updated successfully!"
        
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
            cur.execute("DELETE FROM colleges WHERE college_code = %s",(college_code,))
            if cur.rowcount == 0:
                conn.commit()
                print(f"No college was found with code = {college_code}")
                return False, f"No college was found with code: {college_code}"
            conn.commit()
            return True, "College deleted successfully!"
        except Exception as e:
            conn.rollback()
            print(f"Error deleting college: {e}")
            return False, f"Error deleting college: {e}"
        finally:
            cur.close()