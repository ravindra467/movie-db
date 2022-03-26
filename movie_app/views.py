from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests, imdb

from movie_app.serializers import MovieSerializer
from movie_app.models import Movie

# Create your views here.

API_KEY = "c92837fe"

class search_and_save(APIView):
    def post(self, request):
        search_results_data = []
        query = request.data["query"]
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&s={query}"
        response = requests.get(url)
        try:
            if(response.status_code==200 and response.json()["Response"]!="False"):
                results = response.json()["Search"]
                for result in results:
                    imdbId = result["imdbID"][2:]

                    # creating instance of IMDb
                    ia = imdb.IMDb()
                    series = ia.get_movie(imdbId)
                    rating = series.data['rating']
                    data = {
                        'title': result["Title"], 
                        'year_published': result["Year"], 
                        'imdbId': imdbId, 
                        'imdbRating': rating
                    }
                    search_results_data.append(data)
                    serializer = MovieSerializer(data=data)
                    if(serializer.is_valid()):
                        serializer.save()
        except Exception as e:
            # Sending a blank list with no found movie
            return Response(data=[], status=status.HTTP_201_CREATED)
        
        return Response(data=search_results_data, status=status.HTTP_200_OK)

class get_all_movies(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serilaizers = MovieSerializer(movies, many=True)
        return Response(data=serilaizers.data, status=status.HTTP_200_OK)

class get_top_rated_movies(APIView):
    def get(self, request):
        year_query = request.query_params.get("year")
        movies = Movie.objects.filter(year_published=year_query)
        movies_list = list(MovieSerializer(movies, many=True).data)
        # Sorting the movies based on the imdb rating in decreasing order
        movies_list.sort(key=lambda movie: -float(movie["imdbRating"]))
        return Response(data=movies_list, status=status.HTTP_200_OK)

class movie(APIView):
    def get(self, request, imdbId):
        try:
            movie = Movie.objects.get(imdbId=imdbId)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, imdbId):
        try:
            movie = Movie.objects.get(imdbId=imdbId)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        data["imdbId"] = imdbId
        serializer = MovieSerializer(movie, data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
