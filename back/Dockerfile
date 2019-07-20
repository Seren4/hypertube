FROM python:3.7.3-slim-stretch
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install mysql-server libmariadbclient-dev mysql-client gcc python3-dev netcat nginx -y
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir -p /app /opt/entrypoint/
WORKDIR /app
ADD entrypoint.sh /opt/entrypoint/

ENTRYPOINT ["/bin/bash", "/opt/entrypoint/entrypoint.sh"]
