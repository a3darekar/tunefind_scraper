from django.shortcuts import render

from api.models import Movie, MovieTracks, Show, Season, Episode, SeriesTracks



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

