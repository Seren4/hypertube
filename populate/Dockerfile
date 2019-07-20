FROM debian:stretch

RUN apt-get update && apt-get install -y wget python3 python3-pip nginx netcat 

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /app
COPY ./app /app/
WORKDIR /app
RUN pip3 install -r requirements.txt


ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN mkdir -p /app /opt/entrypoint/
ADD entrypoint.sh /opt/entrypoint/

ENTRYPOINT ["/bin/bash", "/opt/entrypoint/entrypoint.sh"]