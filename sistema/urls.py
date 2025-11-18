from django.contrib import admin
from django.urls import path
from sistema.views import (
    home_view,
    movies_view,
    add_review,
    add_movie,
    my_reviews,
    login_view,
    register_view,
    logout_view
)

urlpatterns = [
    path('', home_view, name='home'),

    path('movies/', movies_view, name='movies'),
    path('movies/add/', add_movie, name='add_movie'),
    path('reviews/mine/', my_reviews, name='my_reviews'),

    path('review/add/<int:movie_id>/', add_review, name='add_review'),
    

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('admin/', admin.site.urls),
]

