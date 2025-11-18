from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción", blank=True)
    year = models.PositiveIntegerField("Año", default=2024)  # ← CORREGIDO
    genre = models.CharField("Género", max_length=50, default="Aventura")
    created_at = models.DateTimeField("Creada el", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Película"
        verbose_name_plural = "Películas"

    def __str__(self):
        return f"{self.title} ({self.year})"


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Película",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Usuario",
    )
    rating = models.PositiveSmallIntegerField("Calificación", help_text="Del 1 al 5")
    comment = models.TextField("Comentario")
    created_at = models.DateTimeField("Creada el", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"Reseña de {self.user.username} para {self.movie.title}"

