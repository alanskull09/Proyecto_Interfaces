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
    
    # ======================================================
# API PARA CHATBOT (SIN DRF, SOLO DJANGO PURO)
# ======================================================
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def api_movies(request):
    movies = Movie.objects.all().order_by('-created_at')
    data = []

    for m in movies:
        data.append({
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "year": m.year,
            "genre": m.genre,
            "created_at": m.created_at.isoformat(),
        })

    return JsonResponse(data, safe=False)


def api_movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all().order_by('-created_at')

    data = []
    for r in reviews:
        data.append({
            "id": r.id,
            "movie_id": movie.id,
            "user": r.user.username,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat(),
        })

    return JsonResponse(data, safe=False)


def api_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')

    data = []
    for r in reviews:
        data.append({
            "id": r.id,
            "movie_title": r.movie.title,
            "movie_id": r.movie.id,
            "user": r.user.username,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat(),
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def api_add_movie(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        body = json.loads(request.body)
        movie = Movie.objects.create(
            title=body["title"],
            description=body.get("description", ""),
            year=body["year"],
            genre=body.get("genre", "Aventura"),
        )
        movie.save()

        return JsonResponse({"status": "ok", "id": movie.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def api_add_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        body = json.loads(request.body)

        movie = Movie.objects.get(id=body["movie_id"])

        user = request.user if request.user.is_authenticated else None

        review = Review.objects.create(
            movie=movie,
            user=user,
            rating=body["rating"],
            comment=body["comment"]
        )
        review.save()

        return JsonResponse({"status": "ok", "id": review.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


