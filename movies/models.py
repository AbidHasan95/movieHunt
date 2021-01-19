from django.db import models

# Create your models here.
class Movie(models.Model):
    ranking = models.DecimalField(max_digits=4,decimal_places=0,null=False)
    movie = models.CharField(max_length=100,null=False)
    rating = models.DecimalField(max_digits=3,decimal_places=1,null=False)
    metascore = models.DecimalField(max_digits=3,decimal_places=0,null=True)
    certification = models.CharField(max_length=30,null=True)
    year = models.DecimalField(max_digits=4,decimal_places=0,null=False)
    runtime = models.DecimalField(max_digits=3,decimal_places=0,null=False)
    genre = models.CharField(max_length=200)
    directors = models.CharField(max_length=200)
    actors = models.CharField(max_length=200)
    votes = models.DecimalField(max_digits=20,decimal_places=0)
    release_date = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    synopsis = models.CharField(max_length=2000,null=True)
    storyline = models.CharField(max_length=3000,null=True)
