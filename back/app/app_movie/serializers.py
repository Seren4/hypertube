from rest_framework import serializers
from app_auth.serializers import *
from app_auth.models import *
from .models import Comment, Movie, Genre, Medias, Seen

from django.contrib.auth.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'id')


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    vu = serializers.SerializerMethodField('get_seen')


    class Meta:
        model = Movie
        read_only_fields = ('vu',)
        fields = ('id','imdb_id','title', 'synopsis', 'year', 'thumbnail', 'rating_yts', 'rating_pop_corn', 'rating_tmdb', 'genre', 'vu')

    def get_seen(self, obj):
        return Seen.objects.filter(user_id=self.context.get("user_id"), movie_id=obj.id).exists()


class MediasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medias
        fields = '__all__'

class ProfileCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'photo', 'photo_url', 'language')


class UserCommentSerializer(serializers.ModelSerializer):
    profile = ProfileCommentSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile', )


class CommentSerializer(serializers.ModelSerializer):

    user = UserCommentSerializer(source='owner', required=False, read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'text', 'created', 'movie_id', 'user')




