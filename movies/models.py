from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Movie(models.Model):
	uid = models.CharField(max_length=10, primary_key=True)
	title = models.CharField(max_length=200)
	sorted_title = models.CharField(max_length=200)
	original_title = models.CharField(max_length=200,null=True,blank=True)
	production_year = models.DateField()
	director = models.CharField(max_length=200)
	poster = models.URLField(blank=True)

	def __str__(self):
		return self.title

	def prod_year(self):
		return self.production_year.year
	
	def viewcount(self):
		return self.movieview_set.all().count()

	def viewrating(self):
		ratings = self.movieview_set.filter(rating__isnull=False)
		if ratings.count() > 0:
			temp_total = 0
			for r in ratings: temp_total += r.rating
			return round(float(temp_total) / ratings.count(), 1)
		else:
			return "No ratings"
		
class MovieView(models.Model):
	uid = models.ForeignKey(Movie, on_delete=models.CASCADE)
	view_date = models.DateField()
	rating = models.PositiveSmallIntegerField(null=True,blank=True,validators=[MaxValueValidator(10)])
	viewer = models.CharField(max_length=100,null=True,blank=True)
	ip = models.GenericIPAddressField(default='127.0.0.1')

	def __str__(self):
		return self.view_date.strftime("%Y-%m-%d")

class MovieListTitle(models.Model):
	year = models.CharField(max_length=4, primary_key=True)
	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title
