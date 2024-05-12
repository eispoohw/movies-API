from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class SingleMovieSerializer(serializers.Serializer):
    movie = MovieSerializer()


class ListMovieSerializer(serializers.Serializer):
    list = MovieSerializer(many=True)


class ErrorSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=500)
    reason = serializers.CharField(default="Ошибка")
