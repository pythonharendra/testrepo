from django.test import TestCase

# Create your tests here.


# [Unit]
# Description=gunicorn daemon
# Requires=gunicorn.socket
# After=network.target

# [Service]
# User=ubuntu
# Group=www-data
# WorkingDirectory=/home/ubuntu/project/social_project
# ExecStart=/home/ubuntu/project/env/bin/gunicorn \
#           --access-logfile - \
#           --workers 3 \
#           --bind unix:/run/gunicorn.sock \
#           socialproject.wsgi:application

# [Install]
# WantedBy=multi-user.target