package main

import (
	"time"
	"github.com/jinzhu/gorm"
)

type Movie struct {
	ID			int64
	ImdbID 		string
	Title 		string
}

type Seen struct {
	ID			int64
	MovieID 		string
	UserID 		string
}

type Medias struct {
	gorm.Model
	MovieID		int64 `gorm:"unique;not null"`
	Hash		string `gorm:"unique;not null"`
	FilePath	string `gorm:"unique;not null"`
	SubEnPath	string 
	SubFrPath	string 
	Extension	string
	Percentage		string
	DownloadRate 	string
	LastSeen	time.Time
}

func (Movie) TableName() string {
	return "movie"
}

func (Seen) TableName() string {
	return "seen"
}