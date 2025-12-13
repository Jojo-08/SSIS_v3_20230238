import re
from app.database import get_db

class Program:
     
    def __init__(self, program_code, program_name, college_code):
        self.program_code = program_code
        self.program_name = program_name
        self.college_code = college_code
        
  

    def get_all(page=1, per_page=20, sort_by='program_code', sort_order='asc', filters=None):
        conn = get_db()
        cur = conn.cursor()
        offset = (page - 1) * per_page
        
        # Whitelist allowed columns to prevent SQL injection
        allowed_columns = ['program_code', 'program_name', 'college_code']
        if sort_by not in allowed_columns:
            sort_by = 'program_code'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'
        
        # Build WHERE clause based on filters
        where_clauses = []
        params = []
        
        if filters:
            if filters.get('college_code'):
                where_clauses.append("college_code = %s")
                params.append(filters['college_code'])
        
        base_query = "SELECT * FROM programs"
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)
        
        query = f"{base_query} ORDER BY {sort_by} {sort_order.upper()} LIMIT %s OFFSET %s"
        params.extend([per_page, offset])
        
        cur.execute(query, tuple(params))
        programs = cur.fetchall()
        cur.close()
        return programs

    def get_total_num(filters=None):
        conn = get_db()
        cur = conn.cursor()
        
        # Build WHERE clause based on filters
        where_clauses = []
        params = []
        
        if filters:
            if filters.get('college_code'):
                where_clauses.append("college_code = %s")
                params.append(filters['college_code'])
        
        base_query = "SELECT COUNT(*) as count FROM programs"
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)
        
        cur.execute(base_query, tuple(params) if params else None)
        total = cur.fetchone()['count']
        cur.close()
        return total

    def get_program(program_code):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM programs WHERE program_code = %s", (program_code,))
        program = cur.fetchone()
        cur.close()
        return program

    def add_program(self):
        
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO programs (program_code, program_name, college_code) 
                        VALUES(%s,%s,%s)""",
                        (self.program_code, self.program_name, self.college_code))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(f"Error adding program: {e}")
            return False
        finally:
            cur.close()

    def edit_program(self, old_program_code):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE programs 
                        SET program_code = %s, program_name = %s, college_code = %s
                        WHERE program_code = %s""",
                        (self.program_code, self.program_name, self.college_code, old_program_code))
            
            if cur.rowcount == 0:
                conn.commit()
                print(f"No program was found with code = {old_program_code}")
                return False, f"No program was found with code: {old_program_code}"
            conn.commit()
            return True, "Program updated successfully!"
        
        except Exception as e:
            conn.rollback()
            print(f"Error updating program: {e}")
            return False, f"Error updating program: {e}"
        finally:
            cur.close()

    def delete_program(program_code):
        conn = get_db()
        cur = conn.cursor()
        try: 
            cur.execute("DELETE FROM programs WHERE program_code = %s",(program_code,))
            if cur.rowcount == 0:
                conn.commit()
                print(f"No program was found with code = {program_code}")
                return False, f"No program was found with code: {program_code}"
            conn.commit()
            return True, "Program deleted successfully!"
        except Exception as e:
            conn.rollback()
            print(f"Error deleting program: {e}")
            return False, f"Error deleting program: {e}"
        finally:
            cur.close()