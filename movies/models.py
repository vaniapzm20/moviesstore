from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class MostPurchasedMovie(Movie):
    class Meta:
        proxy = True
        verbose_name = 'Most Purchased Movie'
        verbose_name_plural = 'Most Purchased Movies'
        
    @admin.display(description="Total Purchases")
    def get_total_purchases(self):
        return self.item_set.count()

class MostReviewedMovie(Movie):
    class Meta:
        proxy = True
        verbose_name = 'Most Reviewed Movie'
        verbose_name_plural = 'Most Reviewed Movies'

    @admin.display(description="Total Reviews")
    def get_total_reviews(self):
        return self.review_set.count()