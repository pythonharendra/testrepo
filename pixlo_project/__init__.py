[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/sammy/testrepo
ExecStart=/home/ubuntu/testrepo/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          pixlo_project.wsgi:application

[Install]
WantedBy=multi-user.target