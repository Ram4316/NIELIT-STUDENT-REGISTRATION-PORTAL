#!/bin/bash
# Update system
sudo yum update -y

# Install Python and MySQL client
sudo yum install -y python3 python3-pip mysql

# Install Flask and MySQL connector
sudo pip3 install flask pymysql

# Create app directory
mkdir -p /home/ec2-user/my-app
cd /home/ec2-user/my-app

# Note: app.py and templates/ will be uploaded manually