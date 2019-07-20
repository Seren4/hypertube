from rest_framework import viewsets
from .serializers import *
from .models import Comment, Movie, Genre, Medias, Torrent, Seen
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, permission_classes
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from django.views import View



from django.db.models import Count, Max

import requests




# ModelViewSet class in order to get the complete set of default read and write operations.
class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, CommentSerializer):
        CommentSerializer.save(owner=self.request.user)

    def retrieve(self, request, pk=None):
        if is_number(pk):
            queryset = Comment.objects.filter(movie_id=pk).order_by('-created')
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response([])

# exclude uncomplete films
def valid_movies():
    movies = Movie.objects.all()
    # movies = Movie.objects.all().filter(imdb_id__isnull=False, thumbnail__isnull=False, year__isnull=False, rating_tmdb__isnull=False).order_by('-year')
    movies = movies.exclude(imdb_id__isnull=True)
    movies = movies.exclude(thumbnail__isnull=True)
    movies = movies.exclude(year__isnull=True)
    movies = movies.exclude(rating_tmdb__isnull=True)
    movies = movies.exclude(genre__isnull=True)
    return (movies)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=False, methods=['GET'], name='Get all movies')
    def page(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)

        if not is_number(page):
            page = 1

        movies = valid_movies().filter(rating_tmdb__gte=8).order_by('-year')
        paginator = Paginator(movies, 30)

        if int(page) >= paginator.num_pages and int(page) != 1:
            return Response({"success":False, "message":"limit reached"})

        try:
            page_result = paginator.page(page)
        except PageNotAnInteger:
            page_result = paginator.page(1)
        except EmptyPage:
            return Response({"success":False})

        result = MovieSerializer(page_result, many=True, context={'user_id': request.user.id}).data
        return Response({"success":True, "movies":result})

    @action(detail=False, methods=['GET'], name='Filter movies')
    def filter(self, request, *args, **kwargs):

        movies = valid_movies().order_by('title')
        title = request.GET.get('title', None)
        year_min = request.GET.get('year_min', None)
        year_max = request.GET.get('year_max', None)
        rating_min = request.GET.get('rating_min', None)
        rating_max = request.GET.get('rating_max', None)
        genre = request.GET.get('genre', None)
        sort = request.GET.get('sort', None)
        page = request.GET.get('page', 1)

        sorts = ['year', 'rating', 'title']

        if not is_number(page):
            page = 1


        check_year = year_min is not None and year_max is not None and year_min != '' and year_max != '' and is_number(year_min) and is_number(year_max)
        check_rating = rating_min is not None and rating_max is not None and rating_min != '' and rating_max != '' and is_float(rating_min) and is_float(rating_max)
        check_sort = sort is not None and sort != '' and sort in sorts

        if title is not None and title != '':
            movies = movies.filter(title__icontains=title)
        if  check_year:
            movies = movies.filter(year__lte=int(year_max), year__gte=int(year_min))
        if genre is not None and genre != '':
            movies = movies.filter(genre__name=genre)
        if check_rating:
            movies = movies.filter(rating_tmdb__lte=float(rating_max), rating_tmdb__gte=float(rating_min))
        if check_sort:
            if sort == 'year':
                sort = '-' + sort
            elif sort == 'rating':
                sort = '-rating_tmdb'
            movies = movies.order_by(sort)
        else:
            movies = movies.order_by('title')

        if movies is not None:
            paginator = Paginator(movies, 30)
            if int(page) >= paginator.num_pages and int(page) != 1:
                return Response({"success": False})

            try:
                page_result = paginator.page(page)
            except PageNotAnInteger:
                page_result = paginator.page(1)
            except EmptyPage:
                return Response({"success": False})
            result = MovieSerializer(page_result, many=True, context={'user_id': request.user.id}).data

            return Response({"success": True, "movies": result})
        return Response({"success": False})

    @action(detail=False, methods=['GET'], name='Sort movies')
    def sort(self, request, *args, **kwargs):

        type = request.GET.get('type', None)
        page = request.GET.get('page', 1)
        sorts = ['year', 'rating', 'title']

        if not is_number(page):
            page = 1

        check_sort = type is not None and type != '' and type in sorts
        if check_sort:
            if type == 'genre':
                type = 'genre__name'
            elif type == 'rating':
                type = '-rating_tmdb'
            if type == 'year':
                type = '-' + type
            movies = valid_movies().order_by(type)
        else:
            movies = valid_movies().order_by('title')

        if movies is not None:
            paginator = Paginator(movies, 30)

            if int(page) >= paginator.num_pages and int(page) != 1:
                return Response({"success": False})

            try:
                page_result = paginator.page(page)
            except PageNotAnInteger:
                page_result = paginator.page(1)
            except EmptyPage:
                return Response({"success": False})

            result = MovieSerializer(page_result, many=True, context={'user_id': request.user.id}).data

            return Response({"success": True, "movies": result})
        return Response({"success": False})

    @action(detail=False, methods=['GET'], name='Get movie')
    def movie(self, request):
        id = request.GET.get('id', None)

        check_id = id is not None and id != '' and is_number(id)
        if check_id == False:
            return Response({"success": False})
        try:
            movie = Movie.objects.get(id=id)
            movie = MovieSerializer(movie).data
            return Response({"success": True, "movie":movie})
        except Movie.DoesNotExist:
            return Response({"success": False})

    @action(detail=False, methods=['GET'], name='Get genres')
    def genre(self, request, *args, **kwargs):
        genres = Genre.objects.values_list('name', flat=True).distinct()
        if genres is not None:
            return Response({"success": True, "genres": genres})
        return Response({"success": False})


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False



class PlayerView(viewsets.ModelViewSet):
    queryset = Medias.objects.all()
    serializer_class = MediasSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'], name='Start Player')
    def start(self, request, *args, **kwargs):
        movie_id = request.GET.get('id', None)
        if movie_id is None:
            return JsonResponse({"success": False, "message": "Movie id parameter is incorrect"})
        media = Medias.objects.filter(movie_id=movie_id)
        movie = Movie.objects.filter(pk=movie_id)
        if media.exists():
            Seen.objects.update_or_create(movie=movie.first(), user=request.user, defaults={"movie": movie.first(), "user": request.user})
            return JsonResponse({"success": True, "media_id": media.first().pk, "fr": media.first().sub_fr_path, "en": media.first().sub_en_path})
        if not movie.exists():
            return JsonResponse({"success": False, "message": "The movie id does not exist in database"})
        imdb_id = movie.first().imdb_id
        torrents = Torrent.objects.filter(movie=movie.first(), quality="720p")
        if not torrents.exists():
            return JsonResponse({"success": False, "message": "No torrent available found for this movie"})
        Seen.objects.update_or_create(movie=movie.first(), user=request.user, defaults={"movie": movie.first(), "user": request.user})
        magnet = torrents.first().magnet
        res = requests.get("http://video:8082/download?magnet={}&imdbid={}".format(magnet, imdb_id))
        if res.status_code == 418:
            return JsonResponse({"success": False, "prout": True, "message": "More than one request at the same time"})
        print("toto")
        res = res.json()
        res.update({"success": True})
        return JsonResponse(res)


