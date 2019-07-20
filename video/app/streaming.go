package main

import (
	"net/http"
	"io"
	log "github.com/sirupsen/logrus"
	"time"
	"strconv"
	"github.com/anacrolix/torrent"
	"github.com/anacrolix/torrent/metainfo"
	"github.com/dustin/go-humanize"
	"path/filepath"
	"strings"
	"encoding/json"
)

func checkIMDBID(imdbID string) bool {
	var movie Movie
	var count int

	db.Where("imdb_id = ?", imdbID).Find(&movie).Count(&count)
	if count != 1 {
		return false
	}
	return true
}

func DownloadMovie() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
	
		magnetURL := r.URL.Query().Get("magnet")
		imdbID := r.URL.Query().Get("imdbid")
		log.Info("[DownloadMovie] - Request received for imdb id : " + imdbID )
		
		ok := checkIMDBID(imdbID) 
		if (!ok) {
			log.Error("[DownloadMovie] - The IMDB id provided does not exist in database")
			w.WriteHeader(http.StatusUnprocessableEntity)
			return
		}

		info, err := metainfo.ParseMagnetURI(magnetURL)
		if err != nil {
			log.Println("[DownloadMovie] - Error while parsing margnet url: " + err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		log.Info("[DownloadMovie] - Magnet parsed: " + magnetURL)
		var media Medias
		var count int
		db.Where("hash = ?", info.InfoHash.HexString()).Find(&media).Count(&count)
		if (count > 1) {
			log.Error("[DownloadMovie] - More than one media requested for download, contact 911")
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		if (count == 1) {
			log.Info("[DownloadMovie] - Media already downloaded")
				data := struct 
				{
					ID uint 		`json:"media_id"`
					French string  	`json:"fr"`
					English string  `json:"en"`
				}{ media.ID, media.SubFrPath, media.SubEnPath }
				db.Model(&media).Update("last_seen", time.Now())
				WriteJSON(w, data)
			WriteJSON(w, data)
			return
		}

		for _, curr := range client.Torrents() {
			if (info.InfoHash.HexString() == curr.InfoHash().HexString()) {
				log.Info("[DownloadMovie] - More than one request at the same time")
				data := struct 
				{
					status bool 		`json:"success"`
					reason string 		`json:"reason"`
				}{ false, "The media is already downloading, please wait"}
				data_res, _ := json.MarshalIndent(data, "", "  ")
				w.WriteHeader(418)
				w.Header().Set("content-type", "application/json; charset=utf-8")
				_, _ = w.Write(data_res)
				return
			}
		}
		log.Info("[DownloadMovie] - The Media is not existing in database, start downloading")
		var t *torrent.Torrent
		if t, err = client.AddMagnet(magnetURL); err != nil {
			log.Error("[DownloadMovie] - Error adding magnet to client: " + err.Error())
			w.WriteHeader(http.StatusInternalServerError)
			return
		}
		log.Info("[DownloadMovie] - Adding trackers to the torrent")
		t.AddTrackers(GetTrackersList())
		log.Info("[DownloadMovie] - Trackers added, waiting to fetch all informations")

		<-t.GotInfo()

		log.Info("[DownloadMovie] - Starting download")
		t.DownloadAll()

		
		file := getLargestFile(t)
		firstPieceIndex := file.Offset() * int64(t.NumPieces()) / t.Length()
		endPieceIndex := (file.Offset() + file.Length()) * int64(t.NumPieces()) / t.Length()
		for idx := firstPieceIndex; idx <= endPieceIndex*15/100; idx++ {
			t.Piece(int(idx)).SetPriority(torrent.PiecePriorityNow)
		}

		log.Info("[DownloadMovie] - Recording a new media in the database")
		var movie Movie
		db.Where("imdb_id = ?", imdbID).First(&movie)
		media = Medias{MovieID: movie.ID, Hash: info.InfoHash.HexString(), LastSeen: time.Now(), FilePath: file.Path(), Extension: strings.TrimPrefix(filepath.Ext(file.Path()), ".")}
		db.Where(Medias{Hash: info.InfoHash.HexString()}).Attrs(media).FirstOrCreate(&media)
		
		log.Info("[DownloadMovie] - Media recorded")
		log.Info("[DownloadMovie] - Fetching and downloading subtitiles")
		getSubtitles(movie, media)
		log.Info("[DownloadMovie] - Subtitles downloaded")

		go func() {
			var progress int64
			for {
				<-time.After(2 * time.Second)
				currentProgress := t.BytesCompleted()
				downloadSpeed := humanize.Bytes(uint64(currentProgress-progress))
				progress = currentProgress
				if percentage(t) < 100 {
					log.Info("[DownloadMovie] - File progression: " + movie.Title + ": " + strconv.Itoa(int(percentage(t))) + "%")
					log.Info("[DownloadMovie] - Download rate: " + downloadSpeed + "/s")
					db.Model(&media).Update("percentage", strconv.Itoa(int(percentage(t))))
					db.Model(&media).Update("download_rate", downloadSpeed)
				} else {
					db.Model(&media).Update("percentage", "100")
					db.Model(&media).Update("download_rate", "0")
					log.Info("[DownloadMovie] - Download finished: " + movie.Title)
					return
				}
			}
		}()

		db.Where(Medias{Hash: info.InfoHash.HexString()}).First(&media)
		for {
			<-time.After(2 * time.Second)
			if percentage(t) > 2 {
				data := struct 
				{
					ID uint `json:"media_id"`
					French string  `json:"fr"`
					English string  `json:"en"`
				}{ media.ID, media.SubFrPath, media.SubEnPath }
				WriteJSON(w, data)
				return
			}
		}
	}
}


func getLargestFile(t *torrent.Torrent) *torrent.File {
	var target *torrent.File
	var maxSize int64

	for _, file := range t.Files() {
		if maxSize < file.Length() {
			maxSize = file.Length()
			target = file
		}
	}
	return target
}

func percentage(t *torrent.Torrent) float64 {
	info := t.Info()
	if info == nil {
		return 0
	}
	return float64(t.BytesCompleted()) / float64(info.TotalLength()) * 100
}

type SeekableContent interface {
	io.ReadSeeker
	io.Closer
}

type FileEntry struct {
	*torrent.File
	torrent.Reader
}


func (f FileEntry) Seek(offset int64, whence int) (int64, error) {
	return f.Reader.Seek(offset+f.File.Offset(), whence)
}


func NewFileReader(f *torrent.File) (SeekableContent, error) {
	torrent := f.Torrent()
	reader := torrent.NewReader()

	reader.SetReadahead(f.Length() / 100)
	reader.SetResponsive()
	_, err := reader.Seek(f.Offset(), io.SeekStart)

	return &FileEntry{
		File:   f,
		Reader: reader,
	}, err
}


func GetStream() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		mediaID := r.URL.Query().Get("media_id")
		log.Info("[GetStream] - Stream request for media: " + mediaID)
		var media Medias
		db.First(&media, mediaID)
		
		if file, ok := client.Torrent(metainfo.NewHashFromHex(media.Hash)); ok {
			target := getLargestFile(file)
			entry, err := NewFileReader(target)
			if err != nil {
				log.Println("[GetStream] - Error opening a new file reader")
				w.WriteHeader(http.StatusInternalServerError)
				return
			}

			defer func() {
				if err := entry.Close(); err != nil {
					log.Println("[GetStream] - Error closing the file reader")
					w.WriteHeader(http.StatusInternalServerError)
					return
				}
			}()

			flusher := w.(http.Flusher)
			flusher.Flush()
			w.Header().Set("Content-Disposition", "attachment; filename=\"" + media.FilePath + "\"")
			http.ServeContent(w, r, target.Path(), time.Now(), entry)
		} else {
			log.Println("[GetStream] - Can't find torrent in torrent client")
			w.WriteHeader(http.StatusNotFound)
			return
		}

	}
}