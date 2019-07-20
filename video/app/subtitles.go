package main

import (
	log "github.com/sirupsen/logrus"
	"strings"
	"github.com/oz/osdb"
	"errors"
	"fmt"
	"strconv"
	"os"
	"os/exec"
)


type MySubtitles struct {
	SubEN osdb.Subtitle
	SubFR osdb.Subtitle
	SubFrFound bool
	SubEnFound bool
}


func initMySubtitles() MySubtitles {
    subs := MySubtitles{}
	subs.SubFrFound = false
	subs.SubEnFound = false
    return subs
}

func getSubtitles(movie Movie, media Medias) {
			osdbClient, err := osdb.NewClient()
			if err != nil {
				log.Info("[getSubtitles] - Error creating OSDB client: " + err.Error())
				return
			}

			if err = osdbClient.LogIn("hypertubo", "le101", "eng"); err != nil {
				log.Info("[getSubtitles] - OSDB LogIn Error: " + err.Error())
				return
			}
			languages := []string{"fre", "eng"}

			res, err := osdbClient.IMDBSearchByID([]string{strings.TrimPrefix(movie.ImdbID, "tt")}, languages)

			if err != nil {
				log.Info("[getSubtitles] - Error with osdbClient.IMDBSearchByID call: " + err.Error())
				return
			}

			subs := initMySubtitles()
			for _, sub := range res {

				if (sub.LanguageName == "French") {
					if subs.SubFrFound == false {
						subs.SubFR = sub
						subs.SubFrFound = true
						continue
					}
					max, _ := strconv.ParseFloat(subs.SubFR.SubRating, 64)
					current, _ := strconv.ParseFloat(sub.SubRating, 64)
					if (current > max) {
						subs.SubFR = sub
					} 
				}

				if (sub.LanguageName == "English") {
					if subs.SubEnFound == false {
						subs.SubEN = sub
						subs.SubEnFound = true
						continue
					}
					max, _ := strconv.ParseFloat(subs.SubEN.SubRating, 64)
					current, _ := strconv.ParseFloat(sub.SubRating, 64)
					if (current > max) {
						subs.SubEN = sub
					} 
				}
			}
			if (subs.SubFrFound == true) {
				err = downloadSubtitles(osdbClient, subs.SubFR, media, "fr")
						if err != nil {
							log.Info("[getSubtitles] - Error while downloading french subs: " + err.Error())
						}
			} else {
				log.Info("[getSubtitles] - No french subtitles found")
			}


			if (subs.SubEnFound == true) {
			err = downloadSubtitles(osdbClient, subs.SubEN, media, "en")
				if err != nil {
					log.Info("[getSubtitles] - Error while downloading english subs: " + err.Error())
				}
			} else {
				log.Info("[getSubtitles] - No english subtitles found")
			}
			if err = osdbClient.LogOut(); err != nil {
				log.Info("[getSubtitles] : OSDB LogOut Error: " + err.Error())
				return
			}			
}

func downloadSubtitles(osdbClient *osdb.Client, sub osdb.Subtitle, media Medias, language string) (err error) {
	folderPath := "subtitles/" + fmt.Sprintf("%d", media.ID)
	filePath := folderPath + "/" + sub.SubFileName
	if _, err := os.Stat(folderPath); os.IsNotExist(err) {
    	os.Mkdir(folderPath, 0777)
	}
	if err = osdbClient.DownloadTo(&sub, filePath); err != nil {
		return errors.New("[DownloadSubtitles] : Error with osdbClient.DownloadTo call: " + err.Error())
	}
	srtPath := folderPath + "/" + language + ".vtt"
	var args = []string{"-i", filePath, "-c:s", "webvtt", srtPath}
	if err := exec.Command("ffmpeg", args...).Run(); err != nil {
		return errors.New("[DownloadSubtitles] : Error with executing ffmpeg call: " + err.Error())
	}
	os.Remove(filePath)
	if (language == "fr") {
		db.Model(&media).Update("sub_fr_path", srtPath)
	}
	if (language == "en") {
		db.Model(&media).Update("sub_en_path", srtPath)
	}
	log.Info("[DownloadSubtitles] - " + language + " subtitles downloaded and save in the database")
	return nil
}