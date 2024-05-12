import django.contrib.auth.models
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import Movie
from .serializers import (ErrorSerializer, ListMovieSerializer,
                          MovieSerializer, SingleMovieSerializer)


def request_or_fail(request):
    def inner(*args, **kwargs):
        try:
            return request(*args, **kwargs)
        except Exception as exc:
            return Response(data={"status": 500, "reason": str(exc)}, status=500)

    return inner


class MovieView(ViewSet):
    list_response = openapi.Response("Список фильмов", ListMovieSerializer)
    entity_response = openapi.Response("Фильм", SingleMovieSerializer)
    error_response = openapi.Response("Ошибка запроса", ErrorSerializer)

    @swagger_auto_schema(
        responses={200: list_response, 400: error_response},
        responce_body=ListMovieSerializer,
    )
    @request_or_fail
    def get_list(self, *args, **kwargs):
        movies = Movie.objects.all()
        movies_json = []

        for movie in movies:
            movies_json.append(MovieSerializer(movie).data)

        return Response(status=200, data={"list": movies_json})

    @swagger_auto_schema(
        request_body=SingleMovieSerializer,
        responses={200: entity_response, 400: error_response},
        responce_body=SingleMovieSerializer,
    )
    @request_or_fail
    def create_movie(self, request, *args, **kwargs):
        movie = request.data.get("movie")
        assert isinstance(movie, dict), "Неверный формат запроса"

        existing_movie = Movie.objects.filter(id=movie["id"])
        assert len(existing_movie) == 0, "Фильм с таким идентификатором уже существует"

        created_movie = Movie(**movie)
        created_movie.save()

        movie_json = MovieSerializer(created_movie).data

        return Response(status=200, data={"movie": movie_json})

    @swagger_auto_schema(
        responses={200: entity_response, 400: error_response},
        responce_body=SingleMovieSerializer,
    )
    @request_or_fail
    def get_movie(self, *args, **kwargs):
        movie = Movie.objects.get(id=kwargs.get("pk"))
        movie_json = MovieSerializer(movie).data

        return Response(status=200, data={"movie": movie_json})

    @swagger_auto_schema(
        request_body=SingleMovieSerializer,
        responses={200: entity_response, 400: error_response},
        responce_body=SingleMovieSerializer,
    )
    @request_or_fail
    def patch_movie(self, request, *args, **kwargs):
        print(request.data, args, kwargs, sep="\n")

        movie = Movie.objects.get(id=kwargs.get("pk"))
        movie_to_update = request.data.get("movie")
        assert isinstance(movie_to_update, dict), "Неверный формат запроса"

        for field, value in movie_to_update.items():
            movie.__setattr__(field, value)

        movie.save()
        movie_json = MovieSerializer(movie).data

        return Response(status=200, data={"movie": movie_json})

    @swagger_auto_schema(
        request_body=SingleMovieSerializer,
        responses={200: entity_response, 400: error_response},
        responce_body=SingleMovieSerializer,
    )
    @request_or_fail
    def delete_movie(self, *args, **kwargs):
        movie = Movie.objects.get(id=kwargs.get("pk"))
        movie.delete()
        movie_json = MovieSerializer(movie).data

        return Response(status=202, data={"movie": movie_json})
