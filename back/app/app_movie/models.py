from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    movie_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ('created',)


class Movie(models.Model):
    imdb_id = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    rating_yts = models.CharField(max_length=255, blank=True, null=True)
    rating_pop_corn = models.CharField(max_length=255, blank=True, null=True)
    rating_tmdb = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'movie'


class Genre(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING, related_name='genre')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'genre'


class Torrent(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    quality = models.CharField(max_length=255, blank=True, null=True)
    magnet = models.TextField(blank=True, null=True)
    hash = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'torrent'


class Seen(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    user = models.ForeignKey(User,  models.DO_NOTHING)

    class Meta:
        db_table = 'seen'

class Medias(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    movie_id = models.BigIntegerField(unique=True)
    hash = models.CharField(unique=True, max_length=255)
    file_path = models.CharField(unique=True, max_length=255)
    sub_en_path = models.CharField(unique=True, max_length=255, blank=True, null=True)
    sub_fr_path = models.CharField(unique=True, max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=255, blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medias'
