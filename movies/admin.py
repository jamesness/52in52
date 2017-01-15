from django.contrib import admin

# Register your models here.

from .models import Movie, MovieView, MovieListTitle

class MovieViewsInline(admin.TabularInline):
	model = MovieView
	extra = 1

class MovieAdmin(admin.ModelAdmin):
	inlines = [MovieViewsInline]

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieListTitle)
