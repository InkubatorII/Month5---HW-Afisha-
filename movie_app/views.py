from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

class DirectorListView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorDetailView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer