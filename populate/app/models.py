# -*- coding: utf-8 -*-
# ########################################################################## #
#          _..---...,""-._     ,/}/)                                         #
#       .''        ,      ``..'(/-<     Made By: Maxime "Max" CONNAT         #
#      /   _      {      )         \    Date: 2019-05-22 18:43:03            #
#     ;   _ `.     `.   <         a(                                         #
#   ,'   ( \  )      `.  \ __.._ .: y   Mail: m.connat@gmail.com             #
#  (  <\_-) )'-.____...\  `._   //-'                                         #
#   `. `-' /-._)))      `-._)))                                              #
#     `...'                                                                  #
# ########################################################################## #

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, primary_key=False)
    thumbnail = db.Column(db.String(255), nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    torrents = db.relationship('Torrent', backref='movie', lazy=True)
    genres = db.relationship('Genre', backref='movie', lazy=True)
    rating_yts = db.Column(db.String(255), nullable=True)
    rating_pop_corn = db.Column(db.String(255), nullable=True)
    rating_tmdb = db.Column(db.Float(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Movie %r>' % self.title



class Torrent(db.Model):
    __tablename__ = 'torrent'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    quality = db.Column(db.String(255), nullable=True)
    magnet = db.Column(db.Text, nullable=True)
    hash = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

