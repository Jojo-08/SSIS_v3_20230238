
CREATE TABLE colleges (
    college_code VARCHAR(10) PRIMARY KEY,
    college_name VARCHAR(255)

);

CREATE TABLE programs (
    program_code VARCHAR(10) PRIMARY KEY,
    program_name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10),
    FOREIGN KEY (college_code) REFERENCES colleges(college_code) ON DELETE CASCADE
);

CREATE TABLE students (
    student_id VARCHAR(9)  PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    program_code VARCHAR(10),
    year INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    FOREIGN KEY (program_code) REFERENCES programs(program_code) ON DELETE SET NULL

);

CREATE TABLE users (
    username VARCHAR(10) PRIMARY KEY,
    password VARCHAR(255) NOT NULL

);