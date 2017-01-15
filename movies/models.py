from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Movie(models.Model):
	uid = models.CharField(max_length=10, primary_key=True)
	title = models.CharField(max_length=200)
	original_title = models.CharField(max_length=200,null=True,blank=True)
	production_year = models.DateField()
	director = models.CharField(max_length=200)
	poster = models.URLField(blank=True)

	def __str__(self):
		return self.title

class MovieViews(models.Model):
	uid = models.ForeignKey(Movie, on_delete=models.CASCADE)
	view_date = models.DateField()

	def __str__(self):
		return self.view_date
