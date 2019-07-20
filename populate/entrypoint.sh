#!/bin/bash

HOST=db
PORT=3306

while true
do
	if nc -z $HOST $PORT; then
	    echo "CONNECTED TO DATABASE"
	    break
	else
	    echo "Can't connect to the database retry in 5 seconds"
	    sleep 5
	fi
done

pip3 install -r /app/requirements.txt
rm /etc/nginx/sites-enabled/*
ln -s /app/nginx.conf /etc/nginx/sites-enabled/populate.conf
service nginx restart
gunicorn wsgi:app --bind=0.0.0.0:5001 --reload --access-logfile - --log-level debug --workers 2 --worker-class gevent