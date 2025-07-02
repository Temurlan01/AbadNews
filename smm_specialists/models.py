from django.db import models
import uuid # Для генерации уникальных токенов
from django.core.validators import MinValueValidator, MaxValueValidator # Для ограничения оценки от 1 до 5

class SmmSpecialist(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    photo = models.ImageField(upload_to='specialist_photo/', verbose_name="Фото")
    description = models.TextField(verbose_name="Описание опыта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def average_rating(self):
    # Этот метод будет вычислять среднюю оценку на основе связанных отзывов
    # Пока что вернем 0, потом реализуем логику
        reviews = self.review_set.all()
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return total_rating / reviews.count()
        return 0.0

    @property
    def review_counts(self):
        # Этот метод будет возвращать количество отзывов
        return self.review_set.count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SMM специалист"
        verbose_name_plural = "SMM специалисты"
        ordering = ['-created_at']  # Сортировка по дате создания по умолчанию


class ReviewToken(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name="Уникальный токен")
    smm_specialist = models.ForeignKey(SmmSpecialist, on_delete=models.CASCADE, verbose_name="Кому отзыв")
    client_name = models.CharField(max_length=100, verbose_name="Названия бизнеса")
    is_user = models.BooleanField(default=False, verbose_name="был ли использован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Когда создан")

    def get_review_url(self):
# Ссылка формируется по шаблону: https://abadnews.com/review/submit/<uuid>/
# Для локальной разработки используем 127.0.0.1:8000
        return f"http://127.0.0.1:8000/review/submit/{self.uuid}/"

    def __str__(self):
        return f"Токен для {self.smm_specialist.name} от {self.client_name}"

    class Meta:
        verbose_name = "Токен отзыва"
        verbose_name_plural = "Токены отзывав"
        ordering = ['-created_at']


class Review(models.Model):
    smm_specialist = models.ForeignKey(SmmSpecialist, on_delete=models.CASCADE, verbose_name="кому отзыв")
    client_name = models.CharField(max_length=100, verbose_name="Название бизнеса")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    comment = models.TextField(verbose_name="текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"Отзыв от {self.client_name} для {self.smm_specialist.name} ({self.rating} звезд)"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
