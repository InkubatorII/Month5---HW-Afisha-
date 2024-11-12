from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg, Count


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Director views
class DirectorListView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

# Review views
class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Additional views for listing with extra data
class MovieListWithReviewsView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        movies = self.get_queryset().prefetch_related('reviews')
        data = []

        for movie in movies:
            reviews = movie.reviews.all()
            avg_rating = reviews.aggregate(Avg('stars'))['stars__avg'] or 0
            reviews_data = [{'id': review.id, 'text': review.text, 'stars': review.stars} for review in reviews]

            data.append({
                'id': movie.id,
                'title': movie.title,
                'reviews': reviews_data,
                'average_rating': avg_rating
            })

        return Response(data)

class DirectorListWithMoviesCountView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get(self, request, *args, **kwargs):
        directors = self.get_queryset().annotate(movies_count=Count('movie'))
        data = [
            {
                'id': director.id,
                'name': director.name,
                'movies_count': director.movies_count
            }
            for director in directors
        ]
        return Response(data)