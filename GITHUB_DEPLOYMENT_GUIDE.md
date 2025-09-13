# GitHub Deployment Guide for NIELIT Student Registration Portal

## Overview
This guide will help you deploy your Flask application with a PostgreSQL database to the cloud, making it accessible from anywhere.

## Quick Start: Railway.app Deployment (Recommended)

### Step 1: Prepare Your Code
1. **Use PostgreSQL version**: Rename `app_postgresql.py` to `app.py`
2. **Update requirements**: Use `requirements_postgresql.txt`
3. **Database schema**: Use `init_db_postgresql.sql`

### Step 2: Create GitHub Repository
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: NIELIT Student Registration Portal"

# Create GitHub repository and push
# Go to GitHub.com → New Repository → Create
git remote add origin https://github.com/yourusername/nielit-portal.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Railway.app
1. **Sign up**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **New Project**: Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository**: Choose your `nielit-portal` repository
4. **Add Database**: 
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will automatically create a PostgreSQL database
5. **Configure Environment Variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DB_HOST=your-postgres-host
   DB_USER=postgres
   DB_PASSWORD=your-postgres-password
   DB_NAME=railway
   DB_PORT=5432
   ```
6. **Deploy**: Railway will automatically deploy your app

### Step 4: Initialize Database
1. **Connect to PostgreSQL**: Use Railway's database dashboard
2. **Run SQL Script**: Execute `init_db_postgresql.sql`
3. **Verify**: Check that tables are created

## Alternative: Render.com Deployment

### Step 1: Prepare for Render
1. **Create Procfile**:
   ```
   web: gunicorn app_postgresql:app
   ```

### Step 2: Deploy to Render
1. **Sign up**: Go to [render.com](https://render.com) and connect GitHub
2. **New Web Service**: Connect your GitHub repository
3. **Configure**:
   - **Build Command**: `pip install -r requirements_postgresql.txt`
   - **Start Command**: `gunicorn app_postgresql:app`
4. **Add Database**: Create PostgreSQL database
5. **Environment Variables**: Set database connection variables
6. **Deploy**: Render will build and deploy automatically

## Alternative: Heroku Deployment

### Step 1: Prepare for Heroku
1. **Create Procfile**:
   ```
   web: gunicorn app_postgresql:app
   ```

2. **Create runtime.txt**:
   ```
   python-3.12.0
   ```

### Step 2: Deploy to Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Initialize database
heroku run python -c "import psycopg2; exec(open('init_db_postgresql.sql').read())"
```

## Environment Variables Setup

### Required Variables
```bash
SECRET_KEY=your-secret-key-here
DB_HOST=your-database-host
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
DB_PORT=5432
```

### Optional Variables
```bash
PORT=5000
FLASK_ENV=production
```

## Database Migration from MySQL to PostgreSQL

### Key Changes Made:
1. **Driver**: `pymysql` → `psycopg2-binary`
2. **Connection**: Updated connection parameters
3. **Queries**: Modified for PostgreSQL syntax
4. **Data Types**: Updated for PostgreSQL compatibility

### SQL Differences:
- `AUTO_INCREMENT` → `SERIAL`
- `BOOLEAN` values: `1/0` → `true/false`
- `DATETIME` → `TIMESTAMP`
- String concatenation: `CONCAT()` → `||` or `STRING_AGG()`

## Testing Your Deployment

### 1. Check Application
- Visit your deployed URL
- Test all routes: `/`, `/register`, `/courses`, `/success`

### 2. Test Database
- Submit a registration form
- Check if data is saved in database
- Verify success page shows correct information

### 3. Monitor Logs
- Check application logs for errors
- Monitor database connections
- Verify environment variables are set correctly

## Troubleshooting

### Common Issues:
1. **Database Connection Failed**
   - Check environment variables
   - Verify database is running
   - Check firewall settings

2. **Import Errors**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

3. **Template Errors**
   - Verify all template files are included
   - Check file paths and permissions

### Debug Mode:
```python
# For local testing
app.run(debug=True)

# For production
app.run(debug=False)
```

## Cost Comparison

| Platform | Free Tier | Paid Plans | Database |
|----------|-----------|------------|----------|
| Railway | 500 hours/month | $5/month | PostgreSQL included |
| Render | 750 hours/month | $7/month | PostgreSQL included |
| Heroku | No free tier | $5/month | PostgreSQL addon |
| GitHub Pages | Free | N/A | Static only |

## Next Steps

1. **Choose your platform** (Railway recommended)
2. **Set up GitHub repository**
3. **Deploy using the guide above**
4. **Test thoroughly**
5. **Share your live application URL**

## Support

- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **Heroku Docs**: https://devcenter.heroku.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs
