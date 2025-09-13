# AWS Deployment Guide

## Quick AWS Deployment Steps

1. **EC2 Instance**: Launch t2.micro instance with Amazon Linux
2. **RDS Database**: Create MySQL database in private subnet
3. **S3 Bucket**: Upload static files (CSS, JS, images)
4. **CloudFront**: Create distribution for S3 content
5. **ALB**: Set up Application Load Balancer
6. **Auto Scaling**: Configure auto scaling group

## Environment Variables for AWS

```bash
DB_HOST=your-rds-endpoint.amazonaws.com
DB_USER=admin
DB_PASSWORD=your-secure-password
DB_NAME=nielit_portal
CLOUDFRONT_URL=https://your-cloudfront-domain.cloudfront.net
```

## Database Setup

Run the SQL script in `(Run this on your RDS instance after creation)/init_db.sql` on your RDS instance.

## Security Groups

- **Web Server**: Allow HTTP (80), HTTPS (443), SSH (22)
- **Database**: Allow MySQL (3306) from Web Server security group
- **ALB**: Allow HTTP (80), HTTPS (443) from anywhere

## Cost Optimization

- Use t2.micro instances (Free Tier)
- Use db.t3.micro for RDS (Free Tier)
- Use NAT Instance instead of NAT Gateway
- Set up auto-scaling to scale down during low usage
