from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

# Create your views here.
from django.http import HttpResponse, Http404
from django.utils import timezone
from dateutil import parser
import json, urllib, re

from .models import Movie, MovieListTitle
from .forms import MovieSearchForm

omdbapi = "https://www.omdbapi.com/?type=movie&%s=%s"

def mmlt(request, listyear=timezone.now().year):
	movie_list = Movie.objects.filter(movieview__view_date__year=listyear).distinct().order_by('sorted_title')
	try:
		list_title = MovieListTitle.objects.get(year=listyear)
	except MovieListTitle.DoesNotExist:
		list_title = "Master Movie List Thingy:  Someone needs to add a title for this year"

	context = {
		'listyear' : listyear,
		'list_title' : list_title,
		'yearly_movie_list': movie_list,
	}
	return render(request, 'movies/index.html', context)

def moviesearch(request):
	searchstring = request.GET['search'].lower()
	if re.match('^tt\d+$', searchstring):
		response = urllib.urlopen(omdbapi % ('i', searchstring))
		data = json.loads(response.read())
		if data['Response']:
			searchdata = [data]
	else:
		response = urllib.urlopen(omdbapi % ('s', searchstring))
		data = json.loads(response.read())
		if data['Response']:
			searchdata = data['Search']
	if data['Response']:
		context = {
			'searchstring' : searchstring,
			'jsondata' : searchdata,
		}
		return render(request, 'movies/moviesearch.html', context)
	else:
	 return HttpResponse("No results")

def addview(request):
	temp_uid = request.POST['imdbid']
	temp_viewdate = parser.parse(request.POST['viewdate'])
	try:
		m = Movie.objects.get(uid=temp_uid)
		# Already exists, just add a viewing
		m.movieview_set.create(view_date=temp_viewdate)
	except Movie.DoesNotExist:
		# Need to add movie, and a viewing
		response = urllib.urlopen(omdbapi % ('i', temp_uid))
		data = json.loads(response.read())
		if data['Response']:
			m = Movie(
				uid = data['imdbID'],
				title = data['Title'],
				title_sort = data ['Title'],
				production_year = parser.parse(data['Year']),
				director = data['Director'],
			)
			if data['Poster']:
				m.poster = data['Poster']
			m.save()
			m.movieview_set.create(view_date=temp_viewdate)
	return redirect('/movies/')

def testform(request):
	form = MovieSearchForm()
	return render(request, 'movies/testform.html', {'form': form})