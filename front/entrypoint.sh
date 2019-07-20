#!/bin/bash

rm /etc/nginx/sites-enabled/*
ln -s /app/nginx.conf /etc/nginx/sites-enabled/front.conf
service nginx restart
npm install -qy
npm run build
tail -f /var/log/nginx/access.log