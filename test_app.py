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

def get_db_connection():
    try:
        # Use Railway's DATABASE_URL if available, otherwise use individual parameters
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            return psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        else:
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

@app.route('/')
def index():
    return "Hello World! App is working!"

@app.route('/test-db')
def test_db():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM courses")
                result = cursor.fetchone()
                connection.close()
                return f"Database connected! Found {result['count']} courses."
        except Exception as e:
            return f"Database error: {str(e)}"
    else:
        return "Database connection failed!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        selected_courses = request.form.getlist('courses')
        
        # Simple validation
        if not name or not email or not selected_courses:
            return "Missing required fields!"
        
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
                    """, (name, email, '1234567890', '2000-01-01', 'Test', 'Test', 'Test Address', datetime.now()))
                    
                    student_id = cursor.fetchone()['student_id']
                    
                    # Insert student courses
                    for course_code in selected_courses:
                        cursor.execute("""
                            INSERT INTO student_courses (student_id, course_code, registration_date)
                            VALUES (%s, %s, %s)
                        """, (student_id, course_code, datetime.now()))
                    
                    connection.commit()
                    connection.close()
                    
                    return f"Success! Student ID: {student_id}, Courses: {selected_courses}"
                    
            except Exception as e:
                if connection:
                    connection.rollback()
                    connection.close()
                return f"Database error: {str(e)}"
        else:
            return "Database connection failed!"
    
    # GET request - show simple form
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT course_code, title FROM courses WHERE is_active = true LIMIT 5")
                courses = cursor.fetchall()
                connection.close()
        except Exception as e:
            courses = []
    else:
        courses = []
    
    form_html = """
    <h2>Test Registration</h2>
    <form method="POST">
        <p>Name: <input type="text" name="name" required></p>
        <p>Email: <input type="email" name="email" required></p>
        <p>Courses:</p>
    """
    
    for course in courses:
        form_html += f'<p><input type="checkbox" name="courses" value="{course["course_code"]}"> {course["title"]}</p>'
    
    form_html += '<p><button type="submit">Submit</button></p></form>'
    
    return form_html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
