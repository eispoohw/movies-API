from django.urls import path

from .views import MovieView

app_name = "app"

urlpatterns = [
    path("movies/", MovieView.as_view({"get": "get_list", "post": "create_movie"})),
    path(
        "movies/<int:pk>",
        MovieView.as_view(
            {"get": "get_movie", "patch": "patch_movie", "delete": "delete_movie"}
        ),
    ),
]
