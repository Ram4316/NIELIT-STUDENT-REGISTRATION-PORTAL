from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'nielit_student_portal_secret_key_2024'

# Get database config from environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'nielit_portal')
CLOUDFRONT_URL = os.environ.get('CLOUDFRONT_URL', '')  # For static files

def get_db_connection():
    try:
        return pymysql.connect(host=DB_HOST,
                               user=DB_USER,
                               password=DB_PASSWORD,
                               database=DB_NAME,
                               cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone) is not None

@app.route('/')
def index():
    return render_template('index.html', cloudfront_url=CLOUDFRONT_URL)

# Demo courses data for when database is not available
DEMO_COURSES = [
    {'course_id': 1, 'course_code': 'CCC', 'title': 'Course on Computer Concepts', 'description': 'Basic computer literacy course covering fundamentals of computing, internet, and digital literacy', 'duration_months': 3, 'fee': 500.00},
    {'course_id': 2, 'course_code': 'O-Level', 'title': 'O-Level Programming', 'description': 'Foundation course in programming covering C, C++, and basic algorithms', 'duration_months': 6, 'fee': 1200.00},
    {'course_id': 3, 'course_code': 'A-Level', 'title': 'A-Level Advanced Programming', 'description': 'Advanced programming course covering data structures, algorithms, and software engineering', 'duration_months': 12, 'fee': 2500.00},
    {'course_id': 4, 'course_code': 'BCC', 'title': 'Basic Computer Course', 'description': 'Entry-level course for computer beginners covering basic operations and applications', 'duration_months': 2, 'fee': 300.00},
    {'course_id': 5, 'course_code': 'DTP', 'title': 'Desktop Publishing', 'description': 'Course on document design and layout using various publishing software', 'duration_months': 3, 'fee': 800.00},
    {'course_id': 6, 'course_code': 'TALLY', 'title': 'Tally ERP 9', 'description': 'Accounting software training for business and financial management', 'duration_months': 2, 'fee': 600.00},
    {'course_id': 7, 'course_code': 'WEB-DESIGN', 'title': 'Web Design & Development', 'description': 'Complete web development course covering HTML, CSS, JavaScript, and PHP', 'duration_months': 8, 'fee': 1800.00},
    {'course_id': 8, 'course_code': 'DCA', 'title': 'Diploma in Computer Applications', 'description': 'Comprehensive diploma course covering multiple computer applications', 'duration_months': 6, 'fee': 1500.00},
    {'course_id': 9, 'course_code': 'PGDCA', 'title': 'Post Graduate Diploma in Computer Applications', 'description': 'Advanced diploma for graduates covering advanced computer concepts and programming', 'duration_months': 12, 'fee': 3000.00},
    {'course_id': 10, 'course_code': 'ADCA', 'title': 'Advanced Diploma in Computer Applications', 'description': 'Advanced course covering networking, database management, and system administration', 'duration_months': 18, 'fee': 4500.00}
]

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        dob = request.form.get('dob', '')
        qualification = request.form.get('qualification', '')
        highest_qualification = request.form.get('highest_qualification', '')
        selected_courses = request.form.getlist('courses')
        address = request.form.get('address', '').strip()
        
        # Validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append('Name must be at least 2 characters long')
        
        if not validate_email(email):
            errors.append('Please enter a valid email address')
        
        if not validate_phone(phone):
            errors.append('Please enter a valid 10-digit mobile number')
        
        if not dob:
            errors.append('Date of birth is required')
        
        if not qualification:
            errors.append('Current qualification is required')
        
        if not highest_qualification:
            errors.append('Highest qualification is required')
        
        if not selected_courses:
            errors.append('Please select at least one course')
        
        if not address or len(address) < 10:
            errors.append('Address must be at least 10 characters long')
        
        if errors:
            # Get available courses for form
            connection = get_db_connection()
            if connection:
                try:
                    with connection.cursor() as cursor:
                        sql = "SELECT * FROM courses WHERE is_active = 1"
                        cursor.execute(sql)
                        courses = cursor.fetchall()
                    connection.close()
                except Exception as e:
                    courses = DEMO_COURSES
                    flash('Using demo data. Database connection error.', 'warning')
            else:
                courses = DEMO_COURSES
                flash('Using demo data. Database not available.', 'info')
            
            return render_template('register.html', 
                                 courses=courses, 
                                 errors=errors,
                                 form_data=request.form,
                                 cloudfront_url=CLOUDFRONT_URL)
        
        # Save to database or demo mode
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Insert student record
                    sql = """INSERT INTO students (name, email, phone, dob, qualification, 
                             highest_qualification, address, registration_date) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (name, email, phone, dob, qualification, 
                                       highest_qualification, address, datetime.now()))
                    
                    student_id = cursor.lastrowid
                    
                    # Insert course selections
                    for course_id in selected_courses:
                        sql = "INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)"
                        cursor.execute(sql, (student_id, course_id))
                    
                    connection.commit()
                    connection.close()
                    
                    # Store success data in session
                    session['registration_success'] = {
                        'name': name,
                        'email': email,
                        'student_id': student_id,
                        'courses': selected_courses
                    }
                    
                    return redirect(url_for('success'))
                    
            except Exception as e:
                flash('Registration failed. Please try again.', 'error')
                courses = DEMO_COURSES
                return render_template('register.html', 
                                     courses=courses, 
                                     errors=['Database error occurred. Please try again.'],
                                     form_data=request.form,
                                     cloudfront_url=CLOUDFRONT_URL)
        else:
            # Demo mode - simulate successful registration
            student_id = 1000 + len(selected_courses)  # Generate demo student ID
            session['registration_success'] = {
                'name': name,
                'email': email,
                'student_id': student_id,
                'courses': selected_courses
            }
            flash('Demo mode: Registration simulated successfully!', 'info')
            return redirect(url_for('success'))
    
    # GET request - show registration form
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM courses WHERE is_active = 1"
                cursor.execute(sql)
                courses = cursor.fetchall()
                connection.close()
        except Exception as e:
            courses = DEMO_COURSES
            flash('Using demo data. Database connection error.', 'warning')
    else:
        courses = DEMO_COURSES
        flash('Using demo data. Database not available.', 'info')
    
    return render_template('register.html', courses=courses, cloudfront_url=CLOUDFRONT_URL)

@app.route('/success')
def success():
    if 'registration_success' not in session:
        return redirect(url_for('index'))
    
    success_data = session.pop('registration_success')
    
    # Get course details
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                course_ids = success_data['courses']
                if course_ids:
                    placeholders = ','.join(['%s'] * len(course_ids))
                    sql = f"SELECT * FROM courses WHERE course_id IN ({placeholders})"
                    cursor.execute(sql, course_ids)
                    courses = cursor.fetchall()
                else:
                    courses = []
            connection.close()
        except Exception as e:
            # Use demo data for selected courses
            course_ids = success_data['courses']
            courses = [course for course in DEMO_COURSES if str(course['course_id']) in course_ids]
    else:
        # Use demo data for selected courses
        course_ids = success_data['courses']
        courses = [course for course in DEMO_COURSES if str(course['course_id']) in course_ids]
    
    return render_template('success.html', 
                         student_data=success_data, 
                           courses=courses,
                           cloudfront_url=CLOUDFRONT_URL)

@app.route('/courses')
def courses():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM courses WHERE is_active = 1"
                cursor.execute(sql)
                courses = cursor.fetchall()
            connection.close()
        except Exception as e:
            courses = DEMO_COURSES
            flash('Using demo data. Database connection error.', 'warning')
    else:
        courses = DEMO_COURSES
        flash('Using demo data. Database not available.', 'info')
    
    return render_template('courses.html', courses=courses, cloudfront_url=CLOUDFRONT_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
