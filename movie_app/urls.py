from django.urls import path
from . import views

app_name = 'movie_app'
urlpatterns = [
    path("search", views.search_and_save.as_view(), name="search_and_save"),
    path("get_all_movies", views.get_all_movies.as_view(), name="get_all_movies"),
    path("get_top_rated_movies", views.get_top_rated_movies.as_view(), name="get_top_rated_movies"),
    path("movie/<imdbId>", views.movie.as_view(), name="movie"),
]