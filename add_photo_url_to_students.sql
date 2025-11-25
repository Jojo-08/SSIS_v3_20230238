-- Migration script to add photo_url column to students table
ALTER TABLE students ADD COLUMN photo_url VARCHAR(500);
