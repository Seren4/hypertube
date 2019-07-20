FROM debian:9

RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install build-essential nodejs nginx -y 

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /app /opt/entrypoint/
WORKDIR /app

COPY ./app/package.json ./

RUN npm i npm@latest -g
RUN npm install -g @vue/cli @vue/cli-service @vue/cli-plugin-babel vue-template-compiler
RUN npm install -qy

ENV PATH /app/node_modules/.bin:$PATH

EXPOSE 3000

RUN mkdir -p /app /opt/entrypoint/
ADD entrypoint.sh /opt/entrypoint/

ENTRYPOINT ["/bin/bash", "/opt/entrypoint/entrypoint.sh"]

