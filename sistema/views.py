from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ReviewForm, MovieForm
from .models import Movie, Review


# -------------------------------
# INICIO: mostrar reseñas recientes
# -------------------------------
def home_view(request):
    reviews = Review.objects.select_related("movie", "user").order_by('-created_at')
    return render(request, 'index.html', {
        'reviews': reviews
    })


# -------------------------------
# AGREGAR RESEÑA
# -------------------------------
@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    form = ReviewForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies')

    return render(request, 'add_review.html', {
        'form': form,
        'movie': movie
    })


# -------------------------------
# LOGIN
# -------------------------------
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})


# -------------------------------
# REGISTRO
# -------------------------------
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})


# -------------------------------
# LOGOUT
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------------------
# LISTA DE PELÍCULAS
# -------------------------------
def movies_view(request):
    movies = Movie.objects.all().order_by('-created_at')
    return render(request, 'movies.html', {'movies': movies})


# -------------------------------
# AGREGAR PELÍCULA
# -------------------------------
@login_required
def add_movie(request):
    form = MovieForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('movies')

    return render(request, 'add_movie.html', {'form': form})


# -------------------------------
# MIS RESEÑAS
# -------------------------------
@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_reviews.html', {'reviews': reviews})

