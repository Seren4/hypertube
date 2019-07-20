# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sse import sse
from pop_corn import *
from tmdb import *
from models import db, Movie
import pymysql
from datetime import datetime

app = Flask(__name__)
pymysql.install_as_MySQLdb()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://devuser:devpass@db/hypertube'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["REDIS_URL"] = "redis://redis"
app.register_blueprint(sse, url_prefix='/stream')
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    pc = max_page_and_movie_pc()
    tmdb = max_page_and_movie_tmdb()
    return render_template('index.html', yts=None, pc=pc, tmdb=tmdb)


@app.route('/pc')
def pop():
    now = datetime.now()
    nb_page = int(request.args.get('nb_page'))
    get_pc_movies_info(nb_page)
    end = datetime.now()
    return str(end - now)


@app.route('/tmdb')
def tmdb():
    now = datetime.now()
    nb_page = int(request.args.get('nb_page'))
    get_tmdb_movies_info(nb_page)
    end = datetime.now()
    return str(end - now)


@app.route("/total")
def total():
    return str(len(Movie.query.all()))

