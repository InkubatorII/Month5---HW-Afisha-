"""
URL configuration for Afisha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_app.views import (
    DirectorListView, DirectorDetailView,
    MovieListView, MovieDetailView,
    ReviewListView, ReviewDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('directors/', DirectorListView.as_view(), name='director-list'),
    path('directors/<int:pk>/', DirectorDetailView.as_view(), name='director-detail'),
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
