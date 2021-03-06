import re
import requests as requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from youtubesearchpython import VideosSearch
import json

ua = UserAgent()
headers = {'User-Agent': ua.random}

BASE_URL = "https://www.tunefind.com"

content_types = {
	1: "Movie",
	2: "TV Show"
}


def get_tracks(url):
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	tracks = soup.find_all("div", attrs={"class": "SongRow_container__0d2_U"})
	track_urls = []
	for track in tracks:
		title = track.find(class_='SongTitle_link__C19Jt').text,
		artist = track.find(class_='Subtitle_subtitle__k3Fvf').text
		search = VideosSearch(f"{title} {artist}", limit=1).result()
		track_urls.append({
			"link": search['result'][0]['link'],
			"title": title,
			"artist": artist
		})
	return track_urls


def get_episodes(season_url):
	page = requests.get(season_url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	episodes = soup.find_all("h3", attrs={ "class": "EpisodeListItem_title__vXExv"})
	episode_urls = dict()
	for episode in episodes:
		episode_title = episode.a.text.replace(' \u00b7 E', 'E').replace(' \u00b7', ' -')
		episode_url = f"{BASE_URL}{episode.a['href']}"
		tracks = get_tracks(episode_url)
		episode_urls[episode_title] = {
			"link": episode_url,
			"tracks": tracks
		}
	return episode_urls


def get_seasons(url):
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	seasons = soup.find_all("a", attrs={"role": "menuitem"})
	season_urls = dict()
	for season in seasons:
		season_id = re.search(r"-[1-9]+", season['href'])[0].replace('-', '')
		season_url = f"{BASE_URL}{season['href']}"
		episodes = get_episodes(season_url)
		season_urls[season_id] = {
			"link": season_url,
			"episodes": episodes
		}
	return season_urls


def save_results(tracks, request_query):
	with open(f"{request_query}.json", "w") as f:
		json.dump(tracks, f, sort_keys=True, indent=4)


def fetch_links(request_query, content_type, year=None):
	request_query = request_query.replace(" ", "-").lower()
	tracks = []
	content_type = content_types[content_type]
	if content_type == 'Movie':
		url = f"{BASE_URL}/movie/{request_query}-{year}"
		tracks = get_tracks(url)
	elif content_type == 'TV Show':
		url = f"{BASE_URL}/show/{request_query}"
		tracks = get_seasons(url)
	else:
		return "Cannot find specified show/movie in tunefind"
	if tracks:
		# save_results(tracks, request_query)
		return tracks, request_query, year, url
	return "Cannot find specified show/movie in tunefind"
