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
from datetime import datetime


def max_page_and_movie_tmdb():
    data = requests.get("https://api.themoviedb.org/3/movie/popular?api_key={}".format("dfcc7fd8cc1b8c0b5bae5f339b7a27c0"))
    movie_count = int(data.json().get('total_results'))
    nb_page = int(data.json().get('total_pages'))
    return {"count": movie_count, "max_page": nb_page}


def get_tmdb_movies_info(nb_page):
    movie_idx = 0
    for i in range(1, nb_page + 1):
        data = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=dfcc7fd8cc1b8c0b5bae5f339b7a27c0&page={}".format(i))
        if data is None:
            continue
        for movie_json in data.json().get('results'):
            movie_dict = serialize_movie_tmdb(movie_json)
            movie_update_or_create(movie_dict)
            movie_idx += 1
            sse.publish({"message": "{}".format(movie_idx)}, type='current_tmdb')
        sse.publish({"message": "{}".format(prct(i, nb_page))}, type='prct_tmdb')


def serialize_movie_tmdb(json):
    return {
        "title": json.get('title'),
        "year": datetime.strptime(json.get('release_date'), '%Y-%m-%d').year  if json.get('release_date') else None, #ValueError: time data '' does not match format '%Y-%m-%d'
        "thumbnail": 'http://image.tmdb.org/t/p/w780' + json.get('poster_path') if json.get('poster_path') else None,
        "synopsis": json.get('overview') if json.get('overview') else None,
        "rating_tmdb": float(json.get('vote_average')),
    }


def movie_update_or_create(movie_dict):
    movie = Movie.query.filter_by(title=movie_dict.get('title'), year=movie_dict.get('year')).first()
    if movie is None:
        movie = Movie(**movie_dict)
        db.session.add(movie)
    else:
        if movie_dict['thumbnail'] is not None:
            movie.thumbnail = movie_dict['thumbnail']
        if movie_dict['synopsis'] is not None:
            movie.synopsis = movie_dict['synopsis']
        movie.rating_tmdb = movie_dict['rating_tmdb']
    db.session.commit()
