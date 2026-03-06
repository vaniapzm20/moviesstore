from django.contrib import admin
from django.db import models
from .models import Movie, Review, MostPurchasedMovie, MostReviewedMovie
from django.db.models import Count
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    ordering = ['name']
    search_fields = ['name']

if not admin.site.is_registered(Review):
    admin.site.register(Review)

class MostPurchasedMovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_total_purchases']
    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(purchase_count=Count('item')).order_by('-purchase_count')
        max_subquery = qs.values("purchase_count")[:1]
        return qs.filter(purchase_count=max_subquery)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False


class MostReviewedMovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_total_reviews']

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(review_count=Count('review')).order_by('-review_count')
        max_subquery = qs.values("review_count")[:1]
        return qs.filter(review_count=max_subquery)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

admin.site.register(MostPurchasedMovie, MostPurchasedMovieAdmin)
admin.site.register(MostReviewedMovie, MostReviewedMovieAdmin)
