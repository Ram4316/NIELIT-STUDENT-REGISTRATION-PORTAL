CREATE DATABASE IF NOT EXISTS nielit_portal;
USE nielit_portal;

-- Courses table for NIELIT courses
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    duration_months INT DEFAULT 6,
    fee DECIMAL(10,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table for registration
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    dob DATE NOT NULL,
    qualification VARCHAR(100) NOT NULL,
    highest_qualification VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'completed') DEFAULT 'active'
);

-- Junction table for student-course relationships
CREATE TABLE student_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('enrolled', 'completed', 'dropped') DEFAULT 'enrolled',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_course (student_id, course_id)
);

-- Insert NIELIT courses
INSERT INTO courses (course_code, title, description, duration_months, fee) VALUES
('CCC', 'Course on Computer Concepts', 'Basic computer literacy course covering fundamentals of computing, internet, and digital literacy', 3, 500.00),
('O-Level', 'O-Level Programming', 'Foundation course in programming covering C, C++, and basic algorithms', 6, 1200.00),
('A-Level', 'A-Level Advanced Programming', 'Advanced programming course covering data structures, algorithms, and software engineering', 12, 2500.00),
('BCC', 'Basic Computer Course', 'Entry-level course for computer beginners covering basic operations and applications', 2, 300.00),
('DTP', 'Desktop Publishing', 'Course on document design and layout using various publishing software', 3, 800.00),
('TALLY', 'Tally ERP 9', 'Accounting software training for business and financial management', 2, 600.00),
('WEB-DESIGN', 'Web Design & Development', 'Complete web development course covering HTML, CSS, JavaScript, and PHP', 8, 1800.00),
('DCA', 'Diploma in Computer Applications', 'Comprehensive diploma course covering multiple computer applications', 6, 1500.00),
('PGDCA', 'Post Graduate Diploma in Computer Applications', 'Advanced diploma for graduates covering advanced computer concepts and programming', 12, 3000.00),
('ADCA', 'Advanced Diploma in Computer Applications', 'Advanced course covering networking, database management, and system administration', 18, 4500.00);