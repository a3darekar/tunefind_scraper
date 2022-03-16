from django.shortcuts import render
from rest_framework import viewsets, routers
from api.models import Movie, MovieTracks, Show, Season, Episode, SeriesTracks

from api.serializers import MovieSerializer, ShowSerializer, MovieTracksSerializer, EpisodeSerializer, SeasonSerializer, \
	SeriesTracksSerializer


# Create your views here.
from tunefind_scraper import fetch_links


def index(request):
	if request.method == 'POST':
		form_data = request.POST
		print(form_data['request_query'])
		if int(form_data['content_type']) == 2:
			data, _req, _year, tunefind_url = fetch_links(request_query=form_data['request_query'], content_type=int(form_data['content_type']))
			show = Show(title= _req, year=_year, tunefind_url=tunefind_url)
			show.save()
			for number, season_data in data.items():
				season = Season(number=number, show=show, tunefind_url=season_data['link'])
				season.save()
				for title, episode_data in season_data['episodes'].items():
					episode = Episode(title=title, season=season, tunefind_url=episode_data['link'])
					episode.save()
					for track_data in episode_data['tracks']:
						track = SeriesTracks(title=track_data['title'][0], episode=episode, artist=track_data['artist'], tunefind_url=track_data['link'])
						track.save()
		else:
			tracks, _req, _year, tunefind_url = fetch_links(request_query=form_data['request_query'], content_type=int(form_data['content_type']), year=form_data['year'])
			movie = Movie(title= _req, year=_year, tunefind_url=tunefind_url)
			movie.save()
			for track in tracks:
				new_track = MovieTracks(title=track['title'][0], artist=track['artist'], movie=movie, youtube_url=track['link'])
				new_track.save()
		print(_year, _req)
	return render(request, 'form.html')


class MovieViewSet(viewsets.ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer


class MovieTracksViewSet(viewsets.ModelViewSet):
	queryset = MovieTracks.objects.all()
	serializer_class = MovieTracksSerializer


class ShowViewSet(viewsets.ModelViewSet):
	queryset = Show.objects.all()
	serializer_class = ShowSerializer


class SeasonViewSet(viewsets.ModelViewSet):
	queryset = Season.objects.all()
	serializer_class = SeasonSerializer


class EpisodeViewSet(viewsets.ModelViewSet):
	queryset = Episode.objects.all()
	serializer_class = EpisodeSerializer


class SeriesTracksViewSet(viewsets.ModelViewSet):
	queryset = SeriesTracks.objects.all()
	serializer_class = SeriesTracksSerializer


api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register(r'movies', MovieViewSet, basename='movies')
api_router.register(r'movie_tracks', MovieTracksViewSet, basename='movie_tracks')
api_router.register(r'shows', ShowViewSet, basename='shows')
api_router.register(r'seasons', SeasonViewSet, basename='seasons')
api_router.register(r'episodes', EpisodeViewSet, basename='episodes')
api_router.register(r'series_racks', SeriesTracksViewSet, basename='series_racks')
