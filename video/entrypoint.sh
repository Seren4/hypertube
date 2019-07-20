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


go build -o server *.go && ./server