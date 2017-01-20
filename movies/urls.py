from django.conf.urls import url

from . import views

app_name = 'movies'
urlpatterns = [
	url(r'^$', views.mmlt, name='mmlt'),
	url(r'^(?P<listyear>[0-9]{4})/$', views.mmlt, name='mmlt'),
	url(r'^moviesearch/$', views.moviesearch, name='moviesearch'),
	url(r'^addview/$', views.addview, name='addview'),
	url(r'^details/(?P<movie_id>tt[0-9]+)/$', views.movieinfo, name='moviedetails'),
]
