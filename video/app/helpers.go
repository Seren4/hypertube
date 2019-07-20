package main

import (
	"net/http"
	"encoding/json"
	log "github.com/sirupsen/logrus"
	"os"
	"strings"
	"fmt"
	// "github.com/anacrolix/torrent"
	// "github.com/anacrolix/torrent/metainfo"
)

func WriteJSON(w http.ResponseWriter, v interface{}) {
	data, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		log.Println("[WriteJSON] - writeJSON(): " + err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
	w.Header().Set("content-type", "application/json; charset=utf-8")
	_, err = w.Write(data)
	if err != nil {
		log.Println("[WriteJSON] - writeJSON(): " + err.Error())
		w.WriteHeader(http.StatusInternalServerError)
	}
}

func CleanOldMedias() {
	log.Info("[CleanOldMedias] - Deleting files not seen since a month")
	rows, err := db.Raw("SELECT * FROM medias WHERE last_seen < DATE_SUB(NOW(), INTERVAL 1 MONTH)").Rows()
	defer rows.Close()
	if err != nil {
		log.Print(err.Error())
	}
	for rows.Next() {
		var media Medias
		db.ScanRows(rows, &media)
		path := strings.Split(media.FilePath, "/")[0]
		err = os.RemoveAll("downloads/" + path)
		if err != nil {
			log.Println("[Helpers.go] - Error while removing file: " + err.Error())
			return
		}
		sub_path := fmt.Sprintf("subtitles/%d", media.ID)
		err = os.RemoveAll(sub_path)
		if err != nil {
			log.Println("[Helpers.go] - Error while removing file: " + err.Error())
			return
		}
		log.Info("[CleanOldMedias] - Deleting media: " + path)
		for _, curr := range client.Torrents() {
			if (media.Hash == curr.InfoHash().HexString()) {
				curr.Drop()
			}
		}
		db.Unscoped().Delete(&media)
	}
}


func GetTrackersList() [][]string {
	trackersList := make([][]string, 1)
	trackers := make([]string, 160)
	trackers = []string{"udp://glotorrents.pw:6969/announce", "udp://tracker.opentrackr.org:1337/announce", "udp://torrent.gresille.org:80/announce", "udp://tracker.openbittorrent.com:80", "udp://tracker.coppersurfer.tk:6969", "udp://tracker.leechers-paradise.org:6969", "udp://p4p.arenabg.ch:1337", "udp://tracker.internetwarriors.net:1337"}
	trackersList[0] = trackers
	return trackersList
}