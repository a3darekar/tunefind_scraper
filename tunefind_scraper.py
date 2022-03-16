import re

import requests as requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
		track_urls.append({
			"link": f"{BASE_URL}{track.a['href']}",
			"title": track.find(class_='SongTitle_link__C19Jt').text,
			"artist": track.find(class_='Subtitle_subtitle__k3Fvf').text
		})
	return track_urls


def get_episodes(season_url):
	page = requests.get(season_url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	episodes = soup.select('[class*="EpisodeListItem_title"]')
	episode_urls = dict()
	for episode in episodes:
		episode_id = re.search(r"-[1-9]+", episode.a['href'])[0].replace('-', '')
		episode_url = f"{BASE_URL}{episode.a['href']}"
		tracks = get_tracks(episode_url)
		episode_urls[episode_id] = {
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


def get_youtube_links(tracks):
	if isinstance(tracks, list):
		print(type(tracks))
	elif isinstance(tracks, list):
		print(type(tracks))
	else:
		print("incorrect data type:", type(tracks))


def fetch_links(request_query, content_type, year=None):
	request_query = request_query.replace(" ", "-").lower()
	tracks = []
	if content_type == 'Movie':
		url = f"{BASE_URL}/movie/{request_query}-{year}"
		tracks = get_tracks(url)
	elif content_type == 'TV Show':
		url = f"{BASE_URL}/show/{request_query}"
		tracks = get_seasons(url)
	if tracks:
		get_youtube_links(tracks)
	else:
		print("Cannot find specified show/movie in tunefind")
