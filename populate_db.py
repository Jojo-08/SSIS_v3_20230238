"""
Script to populate the database with sample data:
- 10 Colleges
- 30 Programs (3 per college)
- 300 Students (10 per program)
"""

import psycopg2
import psycopg2.extras
import random
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ.get('DB_NAME', 'ssis_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASS', '')
}

# Sample data
COLLEGES = [
    ("CCS", "College of Computer Studies"),
    ("COE", "College of Engineering"),
    ("CBA", "College of Business Administration"),
    ("CAS", "College of Arts and Sciences"),
    ("CON", "College of Nursing"),
    ("CED", "College of Education"),
    ("COL", "College of Law"),
    ("CAF", "College of Agriculture and Forestry"),
    ("CHS", "College of Health Sciences"),
    ("CFD", "College of Fine Arts and Design"),
]

PROGRAMS = [
    # CCS Programs
    ("BSCS", "Bachelor of Science in Computer Science", "CCS"),
    ("BSIT", "Bachelor of Science in Information Technology", "CCS"),
    ("BSIS", "Bachelor of Science in Information Systems", "CCS"),
    # COE Programs
    ("BSCE", "Bachelor of Science in Civil Engineering", "COE"),
    ("BSEE", "Bachelor of Science in Electrical Engineering", "COE"),
    ("BSME", "Bachelor of Science in Mechanical Engineering", "COE"),
    # CBA Programs
    ("BSBA", "Bachelor of Science in Business Administration", "CBA"),
    ("BSA", "Bachelor of Science in Accountancy", "CBA"),
    ("BSMA", "Bachelor of Science in Management Accounting", "CBA"),
    # CAS Programs
    ("BSPS", "Bachelor of Science in Political Science", "CAS"),
    ("BSPY", "Bachelor of Science in Psychology", "CAS"),
    ("BSBIO", "Bachelor of Science in Biology", "CAS"),
    # CON Programs
    ("BSN", "Bachelor of Science in Nursing", "CON"),
    ("BSM", "Bachelor of Science in Midwifery", "CON"),
    ("BSPH", "Bachelor of Science in Public Health", "CON"),
    # CED Programs
    ("BEED", "Bachelor of Elementary Education", "CED"),
    ("BSED", "Bachelor of Secondary Education", "CED"),
    ("BPED", "Bachelor of Physical Education", "CED"),
    # COL Programs
    ("JD", "Juris Doctor", "COL"),
    ("LLB", "Bachelor of Laws", "COL"),
    ("BSLM", "Bachelor of Science in Legal Management", "COL"),
    # CAF Programs
    ("BSAG", "Bachelor of Science in Agriculture", "CAF"),
    ("BSFO", "Bachelor of Science in Forestry", "CAF"),
    ("BSAB", "Bachelor of Science in Agribusiness", "CAF"),
    # CHS Programs
    ("BSPT", "Bachelor of Science in Physical Therapy", "CHS"),
    ("BSOT", "Bachelor of Science in Occupational Therapy", "CHS"),
    ("BSMT", "Bachelor of Science in Medical Technology", "CHS"),
    # CFD Programs
    ("BFA", "Bachelor of Fine Arts", "CFD"),
    ("BSIA", "Bachelor of Science in Interior Design", "CFD"),
    ("BSARCH", "Bachelor of Science in Architecture", "CFD"),
]

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Carolyn", "Patrick", "Janet", "Jack", "Catherine",
    "Dennis", "Maria", "Jerry", "Heather", "Tyler", "Diane", "Aaron", "Ruth"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez"
]

GENDERS = ["Male", "Female"]

def main():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()
    
    try:
        # Insert colleges
        print("Inserting colleges...")
        for code, name in COLLEGES:
            cur.execute(
                "INSERT INTO colleges (college_code, college_name) VALUES (%s, %s) ON CONFLICT (college_code) DO NOTHING",
                (code, name)
            )
        conn.commit()
        print(f"Inserted {len(COLLEGES)} colleges")
        
        # Insert programs
        print("Inserting programs...")
        for code, name, college in PROGRAMS:
            cur.execute(
                "INSERT INTO programs (program_code, program_name, college_code) VALUES (%s, %s, %s) ON CONFLICT (program_code) DO NOTHING",
                (code, name, college)
            )
        conn.commit()
        print(f"Inserted {len(PROGRAMS)} programs")
        
        # Insert students (10 per program = 300 total)
        print("Inserting students...")
        student_count = 0
        years = [2020, 2021, 2022, 2023, 2024]
        program_codes = [p[0] for p in PROGRAMS]
        
        for i in range(300):
            year = random.choice(years)
            student_num = str(i + 1).zfill(4)
            student_id = f"{year}-{student_num}"
            
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            program_code = program_codes[i % len(program_codes)]  # Distribute evenly
            year_level = random.randint(1, 4)
            gender = random.choice(GENDERS)
            
            try:
                cur.execute(
                    """INSERT INTO students (student_id, firstname, lastname, program_code, year, gender, photo_url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (student_id) DO NOTHING""",
                    (student_id, first_name, last_name, program_code, year_level, gender, None)
                )
                student_count += 1
            except Exception as e:
                print(f"Error inserting student {student_id}: {e}")
        
        conn.commit()
        print(f"Inserted {student_count} students")
        
        print("\n✅ Database populated successfully!")
        print(f"   - {len(COLLEGES)} Colleges")
        print(f"   - {len(PROGRAMS)} Programs")
        print(f"   - {student_count} Students")
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
