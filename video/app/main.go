package main

import (
	"os"
	"net/http"
	"github.com/rs/cors"
	"github.com/anacrolix/torrent"
	"github.com/robfig/cron"
	log "github.com/sirupsen/logrus"
	"github.com/jinzhu/gorm"
  	_ "github.com/jinzhu/gorm/dialects/mysql"
)

var db *gorm.DB
var client *torrent.Client

func main() {
	var err error
	db, err = gorm.Open("mysql", "devuser:devpass@tcp(db)/hypertube?charset=utf8mb4&parseTime=True&loc=Local")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	db.AutoMigrate(&Medias{})
	go func() {
			err := os.RemoveAll("./downloads")
			if err != nil {
				log.Println("[Main.go]: Error while removing dowloads folder: " + err.Error())
			}
			os.MkdirAll("./downloads", 0777)
			if err != nil {
				log.Println("[Main.go]: Error while creating dowloads folder:" + err.Error())
			}
			err = os.RemoveAll("./subtitles")
			if err != nil {
				log.Println("[Main.go]: Error while removing dowloads folder: " + err.Error())
			}
			os.MkdirAll("./subtitles", 0777)
			if err != nil {
				log.Println("[Main.go]: Error while creating dowloads folder:" + err.Error())
			}
			db.Unscoped().Delete(&Medias{})
			db.Unscoped().Delete(&Seen{})
	}()
	config := torrent.NewDefaultClientConfig()
	config.DataDir = "./downloads"
	config.NoUpload = true
	config.Seed = false
	config.DisableTCP = false
	config.ListenPort = 50007

	client, err = torrent.NewClient(config)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Close()
	mux := http.NewServeMux()
	fs := http.FileServer(http.Dir("/go/src/video/subtitles"))
	mux.Handle("/subtitles/", http.StripPrefix("/subtitles", fs))
	mux.Handle("/stream", GetStream())
	mux.Handle("/download", DownloadMovie())
	mux.Handle("/info", GetDownloadInfos())
	
	cron := cron.New()
	cron.AddFunc("@every 1m", CleanOldMedias)
	cron.Start()

	c := cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedHeaders: []string{"Authorization", "Content-Type"},
	})
	handler := c.Handler(mux)
	log.Println("Server listening on port 8082")
	log.Fatal(http.ListenAndServe(":8082", handler))
}


func GetDownloadInfos() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		media_id := r.URL.Query().Get("media_id")
		var media Medias
		db.First(&media, media_id)
		data := struct 
			{
				ID uint 		`json:"media_id"`
				Rate string  	`json:"rate"`
				Percentage string  `json:"prct"`
			}{ media.ID, media.DownloadRate, media.Percentage }
			WriteJSON(w, data)
	}
}