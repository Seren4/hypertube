# -*- coding: utf-8 -*-
# ########################################################################## #
#          _..---...,""-._     ,/}/)                                         #
#       .''        ,      ``..'(/-<     Made By: Maxime "Max" CONNAT         #
#      /   _      {      )         \    Date: 2019-05-22 18:43:34            #
#     ;   _ `.     `.   <         a(                                         #
#   ,'   ( \  )      `.  \ __.._ .: y   Mail: m.connat@gmail.com             #
#  (  <\_-) )'-.____...\  `._   //-'                                         #
#   `. `-' /-._)))      `-._)))                                              #
#     `...'                                                                  #
# ########################################################################## #

import requests
import math
from flask_sse import sse
from helpers import prct
from models import db, Movie, Genre, Torrent
import time


def max_page_and_movie_pc():
    data = requests.get("https://tv-v2.api-fetch.website/movies")
    nb_page = int(len(data.json()))
    movie_count = nb_page * 50
    return {"count": movie_count, "max_page": nb_page}


def get_pc_movies_info(nb_page):
    movie_idx = 0
    for i in range(1, nb_page + 1):
        data = requests.get("https://tv-v2.api-fetch.website/movies/{}".format(i))
        if data is None:
            continue
        for movie_json in data.json():
            movie_dict = serialize_movie_pc(movie_json)
            torrent_list = serialize_torrents_pc(movie_json)
            movie_id = movie_update_or_create(movie_dict)
            genre_list = serialize_genres_pc(movie_json)
            if genre_list is not None:
                genre_update_or_create(movie_id, genre_list)
            if torrent_list is not None:
                torrent_update_or_create(movie_id, torrent_list)
            movie_idx += 1
            sse.publish({"message": "{}".format(movie_idx)}, type='current_pc')
        sse.publish({"message": "{}".format(prct(i, nb_page))}, type='prct_pc')


def serialize_movie_pc(json):
    return {
        "imdb_id": json.get('imdb_id'),
        "title": json.get('title'),
        "year": json.get('year'),
        "synopsis": json.get('synopsis'),
        "rating_pop_corn": json.get('rating').get('percentage')
    }

def serialize_torrents_pc(data):
    ret = list()
    files = data.get("torrents", None)
    torrents = files.get("en", None)
    if torrents is None:
            return None
    for quality, torrent in torrents.items():
        ret.append({
            "quality": quality,
            "magnet": torrent.get("url")
        })
    return ret

def serialize_genres_pc(data):
    ret = list()
    genres = data.get("genres", None)
    if genres is None:
            return None
    for genre in genres:
        ret.append({"name": genre})
    return ret


def movie_update_or_create(movie_dict):
    movie = Movie.query.filter_by(title=movie_dict.get('title'), year=movie_dict.get('year')).first()
    if movie is None:
        movie = Movie(**movie_dict)
        db.session.add(movie)
    else:
        movie.rating_pop_corn = movie_dict['rating_pop_corn']
    db.session.commit()
    return movie.id


def genre_update_or_create(movie_id, genre_list):
    genres = Genre.query.filter_by(movie_id=movie_id).all()
    if len(genres) == 0:
        for genre in genre_list:
            genre.update({"movie_id": movie_id})
            new = Genre(**genre)
            db.session.add(new)
        db.session.commit()
    return

def torrent_update_or_create(movie_id, torrent_list):
    torrents = Torrent.query.filter_by(movie_id=movie_id).all()
    if len(torrents) == 0:
        for torrent in torrent_list:
            torrent.update({"movie_id": movie_id})
            new = Torrent(**torrent)
            db.session.add(new)
        db.session.commit()
    return
