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
pip3 install --upgrade mysqlclient
python3 manage.py makemigrations
python3 manage.py makemigrations app_auth
python3 manage.py makemigrations app_movie
python3 manage.py migrate
python3 manage.py migrate app_movie
python3 manage.py migrate app_auth
#python3 manage.py runscript start
rm /etc/nginx/sites-enabled/*
ln -s /app/nginx.conf /etc/nginx/sites-enabled/back.conf
service nginx restart
python3 manage.py collectstatic --noinput
gunicorn back.wsgi:application --bind=0.0.0.0:8001 --reload --access-logfile - --log-level debug --workers 2 --worker-class gevent