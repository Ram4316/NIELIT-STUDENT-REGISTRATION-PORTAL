-- PostgreSQL Database Schema for NIELIT Student Registration Portal
-- Run this script on your PostgreSQL database after creation

-- Create database (run this separately if needed)
-- CREATE DATABASE nielit_portal;

-- Connect to the database
-- \c nielit_portal;

-- Create courses table
CREATE TABLE IF NOT EXISTS courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    duration_months INTEGER NOT NULL,
    fee DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    dob DATE NOT NULL,
    qualification VARCHAR(100) NOT NULL,
    highest_qualification VARCHAR(100) NOT NULL,
    address TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create student_courses junction table
CREATE TABLE IF NOT EXISTS student_courses (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id)
);

-- Insert sample courses
INSERT INTO courses (course_code, title, description, duration_months, fee, is_active) VALUES
('CCC', 'Course on Computer Concepts', 'Basic computer literacy course covering fundamental concepts of computers, operating systems, and basic applications.', 3, 5000.00, true),
('O Level', 'O Level Programming', 'Programming fundamentals covering C, C++, and basic algorithms. Suitable for beginners in programming.', 6, 12000.00, true),
('A Level', 'A Level Programming', 'Advanced programming concepts including data structures, algorithms, and software engineering principles.', 12, 25000.00, true),
('BCC', 'Basic Computer Course', 'Introduction to computers, basic operations, and essential software applications.', 2, 3000.00, true),
('DCA', 'Diploma in Computer Applications', 'Comprehensive computer applications course covering office automation, database management, and basic programming.', 6, 15000.00, true),
('PGDCA', 'Post Graduate Diploma in Computer Applications', 'Advanced computer applications for graduates, covering advanced programming, database design, and system analysis.', 12, 30000.00, true),
('DTP', 'Desktop Publishing', 'Design and publishing software training including Adobe InDesign, Photoshop, and CorelDRAW.', 3, 8000.00, true),
('TALLY', 'Tally ERP 9', 'Comprehensive accounting software training covering financial management, inventory, and taxation.', 2, 6000.00, true),
('WEB', 'Web Development', 'Complete web development course covering HTML, CSS, JavaScript, PHP, and MySQL.', 6, 18000.00, true),
('PYTHON', 'Python Programming', 'Python programming language course covering basics to advanced concepts including frameworks and libraries.', 4, 12000.00, true)
ON CONFLICT (course_code) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_students_phone ON students(phone);
CREATE INDEX IF NOT EXISTS idx_student_courses_student_id ON student_courses(student_id);
CREATE INDEX IF NOT EXISTS idx_student_courses_course_id ON student_courses(course_id);
CREATE INDEX IF NOT EXISTS idx_courses_active ON courses(is_active);

-- Create a view for student enrollment summary
CREATE OR REPLACE VIEW student_enrollment_summary AS
SELECT 
    s.student_id,
    s.name,
    s.email,
    s.phone,
    s.registration_date,
    COUNT(sc.course_id) as total_courses,
    STRING_AGG(c.title, ', ') as enrolled_courses
FROM students s
LEFT JOIN student_courses sc ON s.student_id = sc.student_id
LEFT JOIN courses c ON sc.course_id = c.course_id
GROUP BY s.student_id, s.name, s.email, s.phone, s.registration_date;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
