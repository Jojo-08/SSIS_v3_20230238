CREATE TABLE colleges (
    college_code VARCHAR(10) PRIMARY KEY,
    college_name VARCHAR(255)
);

CREATE TABLE programs (
    program_code VARCHAR(10) PRIMARY KEY,
    program_name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10),
    FOREIGN KEY (college_code) REFERENCES colleges (college_code) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE students (
    student_id VARCHAR(9) PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    program_code VARCHAR(10),
    year INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    photo_url VARCHAR(500),
    FOREIGN KEY (program_code) REFERENCES programs (program_code) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);