from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database configuration for PostgreSQL
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'nielit_portal')
DB_PORT = os.environ.get('DB_PORT', '5432')

# Demo courses data (fallback when database is not available)
DEMO_COURSES = [
    {'course_code': 'CCC', 'title': 'Course on Computer Concepts', 'description': 'Basic computer literacy course', 'duration_months': 3, 'fee': 5000, 'is_active': True},
    {'course_code': 'O Level', 'title': 'O Level Programming', 'description': 'Programming fundamentals', 'duration_months': 6, 'fee': 12000, 'is_active': True},
    {'course_code': 'A Level', 'title': 'A Level Programming', 'description': 'Advanced programming concepts', 'duration_months': 12, 'fee': 25000, 'is_active': True},
    {'course_code': 'BCC', 'title': 'Basic Computer Course', 'description': 'Introduction to computers', 'duration_months': 2, 'fee': 3000, 'is_active': True},
    {'course_code': 'DCA', 'title': 'Diploma in Computer Applications', 'description': 'Comprehensive computer applications', 'duration_months': 6, 'fee': 15000, 'is_active': True},
    {'course_code': 'PGDCA', 'title': 'Post Graduate Diploma in Computer Applications', 'description': 'Advanced computer applications', 'duration_months': 12, 'fee': 30000, 'is_active': True},
    {'course_code': 'DTP', 'title': 'Desktop Publishing', 'description': 'Design and publishing software', 'duration_months': 3, 'fee': 8000, 'is_active': True},
    {'course_code': 'TALLY', 'title': 'Tally ERP 9', 'description': 'Accounting software training', 'duration_months': 2, 'fee': 6000, 'is_active': True},
    {'course_code': 'WEB', 'title': 'Web Development', 'description': 'HTML, CSS, JavaScript, PHP', 'duration_months': 6, 'fee': 18000, 'is_active': True},
    {'course_code': 'PYTHON', 'title': 'Python Programming', 'description': 'Python programming language', 'duration_months': 4, 'fee': 12000, 'is_active': True}
]

def get_db_connection():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )
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
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        dob = request.form.get('dob', '')
        qualification = request.form.get('qualification', '').strip()
        highest_qualification = request.form.get('highest_qualification', '').strip()
        address = request.form.get('address', '').strip()
        selected_courses = request.form.getlist('courses')
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        elif not validate_email(email):
            errors.append('Invalid email format')
        if not phone:
            errors.append('Phone number is required')
        elif not validate_phone(phone):
            errors.append('Invalid phone number (10 digits starting with 6-9)')
        if not dob:
            errors.append('Date of birth is required')
        if not qualification:
            errors.append('Qualification is required')
        if not highest_qualification:
            errors.append('Highest qualification is required')
        if not selected_courses:
            errors.append('Please select at least one course')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('register'))
        
        # Try to save to database
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    # Insert student
                    cursor.execute("""
                        INSERT INTO students (name, email, phone, dob, qualification, highest_qualification, address, registration_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING student_id
                    """, (name, email, phone, dob, qualification, highest_qualification, address, datetime.now()))
                    
                    student_id = cursor.fetchone()['student_id']
                    
                    # Insert student courses
                    for course_code in selected_courses:
                        cursor.execute("""
                            INSERT INTO student_courses (student_id, course_code, registration_date)
                            VALUES (%s, %s, %s)
                        """, (student_id, course_code, datetime.now()))
                    
                    connection.commit()
                    connection.close()
                    
                    # Store success data in session
                    session['registration_success'] = {
                        'student_id': student_id,
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'dob': dob,
                        'qualification': qualification,
                        'highest_qualification': highest_qualification,
                        'address': address,
                        'courses': selected_courses,
                        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    flash('Registration successful!', 'success')
                    return redirect(url_for('success'))
                    
            except Exception as e:
                connection.rollback()
                connection.close()
                flash(f'Database error: {str(e)}', 'error')
                return redirect(url_for('register'))
        else:
            # Demo mode - simulate successful registration
            session['registration_success'] = {
                'student_id': 12345,  # Demo ID
                'name': name,
                'email': email,
                'phone': phone,
                'dob': dob,
                'qualification': qualification,
                'highest_qualification': highest_qualification,
                'address': address,
                'courses': selected_courses,
                'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            flash('Demo mode: Registration simulated successfully!', 'info')
            return redirect(url_for('success'))
    
    # GET request - show registration form
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM courses WHERE is_active = true")
                courses = cursor.fetchall()
                connection.close()
        except Exception as e:
            courses = DEMO_COURSES
            flash('Using demo data. Database connection error.', 'warning')
    else:
        courses = DEMO_COURSES
        flash('Using demo data. Database not available.', 'info')
    
    return render_template('register.html', courses=courses)

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
                course_codes = success_data['courses']
                if course_codes:
                    placeholders = ','.join(['%s'] * len(course_codes))
                    cursor.execute(f"SELECT * FROM courses WHERE course_code IN ({placeholders})", course_codes)
                    courses = cursor.fetchall()
                else:
                    courses = []
                connection.close()
        except Exception as e:
            # Fallback to demo courses
            courses = [course for course in DEMO_COURSES if course['course_code'] in success_data['courses']]
    else:
        # Demo mode
        courses = [course for course in DEMO_COURSES if course['course_code'] in success_data['courses']]
    
    return render_template('success.html',
                         student_data=success_data,
                         courses=courses)

@app.route('/courses')
def courses():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM courses WHERE is_active = true ORDER BY course_code")
                courses = cursor.fetchall()
                connection.close()
        except Exception as e:
            courses = DEMO_COURSES
            flash('Using demo data. Database connection error.', 'warning')
    else:
        courses = DEMO_COURSES
        flash('Using demo data. Database not available.', 'info')
    
    return render_template('courses.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
