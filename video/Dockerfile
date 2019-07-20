FROM golang:1.12.4-stretch

RUN apt-get update && apt-get install ffmpeg netcat -y
RUN go get github.com/anacrolix/torrent 
RUN go get github.com/dustin/go-humanize
RUN go get github.com/sirupsen/logrus
RUN go get github.com/jinzhu/gorm
RUN go get github.com/gorilla/mux
RUN go get github.com/jasonlvhit/gocron
RUN go get github.com/rs/cors
RUN go get github.com/robfig/cron
RUN go get github.com/oz/osdb
RUN go get github.com/go-sql-driver/mysql

ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /go/src/video
RUN mkdir -p /app /opt/entrypoint/
ADD entrypoint.sh /opt/entrypoint/

WORKDIR /go/src/video

ENTRYPOINT ["/bin/bash", "/opt/entrypoint/entrypoint.sh"]
