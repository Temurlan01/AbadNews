from django.contrib import admin
from .models import SmmSpecialist, ReviewToken, Review


@admin.register(SmmSpecialist)
class SmmSpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating', 'review_counts', 'created_at')
    search_fields = ('name', 'description')


@admin.register(ReviewToken)
class ReviewTokenAdmin(admin.ModelAdmin):
    list_display = ('smm_specialist', 'client_name', 'uuid', 'is_user', 'created_at')
    list_filter = ('is_user', 'created_at')
    list_fields = ('smm_specialist__name', 'client_name', 'uuid')
    # Поля, которые не будут редактироваться при создании/редактировании
    readonly_fields = ('uuid', 'created_at', 'get_review_url')
    fields = ('smm_specialist', 'client_name', 'uuid', 'is_used', 'created_at', 'get_review_url') # Порядок полей

    def get_review_url(self, obj):
        return obj.get_review_url()

    get_review_url.short_description = "Ссылка для отзыва"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('smm_specialist', 'client_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('smm_specialist__name', 'client_name', 'comment')
    readonly_fields = ('created_at',)