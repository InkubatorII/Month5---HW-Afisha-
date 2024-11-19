from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import RegistrationSerializer, ConfirmationSerializer, LoginSerializer

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered. Please confirm your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationView(APIView):
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User confirmed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class MovieListWithReviewsView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        movies = self.get_queryset().prefetch_related('reviews')

        if not movies.exists():
            return Response({"detail": "Фильмы не найдены."}, status=status.HTTP_404_NOT_FOUND)

        data = []
        for movie in movies:
            reviews = movie.reviews.all()
            avg_rating = reviews.aggregate(Avg('stars'))['stars__avg'] or 0

            if not reviews.exists():
                reviews_data = []
            else:
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

        # Проверка: Если нет директоров, возвращаем ошибку
        if not directors.exists():
            return Response({"detail": "Режисеры  не найдены."}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                'id': director.id,
                'name': director.name,
                'movies_count': director.movies_count
            }
            for director in directors
        ]

        return Response(data)