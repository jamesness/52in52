from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

# Create your views here.
from django.http import HttpResponse, Http404
from django.utils import timezone
from dateutil import parser
import json, urllib, re

from .models import Movie, MovieListTitle, MovieView
from .forms import MovieSearchForm

omdbapi = "https://www.omdbapi.com/?type=movie&%s=%s"

def mmlt(request, listyear=timezone.now().year):
	movie_list = Movie.objects.filter(movieview__view_date__year=listyear).distinct().order_by('sorted_title')
	view_list = MovieView.objects.filter(view_date__year=listyear)
	try:
		list_title = MovieListTitle.objects.get(year=listyear)
	except MovieListTitle.DoesNotExist:
		list_title = "Master Movie List Thingy:  Someone needs to add a title for this year"

	context = {
		'listyear' : listyear,
		'list_title' : list_title,
		'yearly_movie_list': movie_list,
		'view_list': view_list,
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
				sorted_title = data ['Title'],
				production_year = parser.parse(data['Year']),
				director = data['Director'],
			)
			if data['Poster']:
				m.poster = data['Poster']
			if re.match('^The ',m.title): m.sorted_title = re.sub('^The ','',m.title)
			elif re.match('^A ',m.title): m.sorted_title = re.sub('^A ','',m.title)
			elif re.match('^An ',m.title): m.sorted_title = re.sub('^An ','',m.title)
			else: m.sorted_title = m.title

			m.save()
			m.movieview_set.create(view_date=temp_viewdate)
	return redirect('/movies/')

def movieinfo(request, movie_id):
	movie = Movie.objects.get(pk=movie_id)
	context = {
		'movie': movie,
	}
	return render(request, 'movies/movieinfo.html', context)
	
def testview(request):
	view_list = MovieView.objects.filter(view_date__year=2017)
	context = {
		'view_list': view_list,
	}
	return render(request, 'movies/test.html', context)