# NIELIT Student Registration Portal

A scalable and responsive web application for NIELIT student registration, built with Flask and designed for AWS deployment.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py

# 3. Open browser: http://localhost:5000
```

## 📁 Project Structure

```
AvakashAWS/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # This documentation
├── templates/                     # HTML templates
│   ├── base.html                  # Base template with NIELIT branding
│   ├── index.html                 # Home page
│   ├── register.html              # Registration form
│   ├── success.html               # Success page
│   └── courses.html               # Courses listing
├── static/                        # Static files (CSS, JS, images)
│   └── style.css                  # Main stylesheet
├── AWS-Refined/                   # AWS deployment documentation
│   ├── Aws-Project.md             # Project requirements
│   └── Blueprint.md               # AWS architecture blueprint
├── (Run this on your RDS instance after creation)/
│   └── init_db.sql                # Database schema with NIELIT courses
└── (User Data script for EC2)/
    └── setup.sh                   # AWS EC2 setup script
```

## 🎯 Features

- **Student Registration**: Complete form with validation (Name, DOB, Qualification, etc.)
- **Course Selection**: 10 NIELIT courses with multiple selection
- **Success Page**: "Successfully Registered" confirmation
- **Responsive Design**: Mobile-first approach with #213047 background
- **Demo Mode**: Works without database for testing
- **Form Validation**: Email, phone, required fields validation

## 🎓 Available NIELIT Courses

1. **CCC** - Course on Computer Concepts (₹500)
2. **O-Level** - O-Level Programming (₹1,200)
3. **A-Level** - A-Level Advanced Programming (₹2,500)
4. **BCC** - Basic Computer Course (₹300)
5. **DTP** - Desktop Publishing (₹800)
6. **TALLY** - Tally ERP 9 (₹600)
7. **WEB-DESIGN** - Web Design & Development (₹1,800)
8. **DCA** - Diploma in Computer Applications (₹1,500)
9. **PGDCA** - Post Graduate Diploma in Computer Applications (₹3,000)
10. **ADCA** - Advanced Diploma in Computer Applications (₹4,500)

## 🌐 Access URLs

- **Home Page**: http://localhost:5000
- **Registration Form**: http://localhost:5000/register
- **Courses Page**: http://localhost:5000/courses
- **Success Page**: http://localhost:5000/success (after registration)

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL (with demo mode fallback)
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Deployment**: AWS (EC2, RDS, S3, CloudFront)

## 📱 Testing the Application

1. **Home Page**: View NIELIT information and course highlights
2. **Registration**: Fill out the complete registration form
3. **Course Selection**: Choose from 10 NIELIT courses
4. **Form Validation**: Test with invalid data to see validation
5. **Success Page**: Complete registration to see confirmation
6. **Responsive**: Test on different screen sizes

## 🗄️ Database Setup (Optional)

For full functionality with database:

```bash
# 1. Install MySQL
sudo apt install mysql-server

# 2. Create database
mysql -u root -p -e "CREATE DATABASE nielit_portal;"

# 3. Import schema
mysql -u root -p nielit_portal < "(Run this on your RDS instance after creation)/init_db.sql"

# 4. Update .env file with your MySQL password
echo "DB_PASSWORD=your_password" >> .env
```

## ☁️ AWS Deployment

The application is designed for AWS deployment with:
- **EC2**: Web server hosting
- **RDS**: MySQL database
- **S3**: Static file storage
- **CloudFront**: CDN for static content
- **ALB**: Application Load Balancer
- **Auto Scaling**: Automatic scaling
- **VPC**: Secure network architecture

Refer to `AWS-Refined/Blueprint.md` for detailed AWS deployment instructions.

## 🎨 Design Features

- **NIELIT Branding**: Professional design with government colors
- **Responsive**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean interface with gradients and animations
- **Accessibility**: Proper contrast and readable fonts
- **Form Validation**: Real-time feedback and error handling

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - App works in demo mode without database
   - Install MySQL for full functionality

2. **Port Already in Use**
   - Change port in `app.py` from 5000 to another port

3. **CSS Not Loading**
   - Check if static files are properly referenced
   - For local development, CLOUDFRONT_URL should be empty

### Development Tips

- Use `debug=True` in `app.py` for development
- Check browser console for JavaScript errors
- Test form validation with various inputs
- Use browser developer tools to inspect responsive design

## 📊 Database Schema

### Tables

1. **courses**: Stores available NIELIT courses
2. **students**: Stores student registration information
3. **student_courses**: Junction table for student-course relationships

## 🚀 Production Deployment

For production deployment:
1. Set up MySQL database
2. Configure environment variables
3. Deploy to AWS following Blueprint.md
4. Set up monitoring and logging
5. Configure SSL certificates

## 📞 Support

- **Documentation**: This README file
- **AWS Guide**: AWS-Refined/Blueprint.md
- **Database Schema**: (Run this on your RDS instance after creation)/init_db.sql

---

**🎉 The NIELIT Student Registration Portal is ready for use!**

**Access it at: http://localhost:5000**
