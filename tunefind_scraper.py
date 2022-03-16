import re

import requests as requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent': ua.random}

BASE_URL = "https://www.tunefind.com"

content_types = {
	1: "Movie",
	2: "Show"
}


def get_tracks(url):
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	tracks = soup.find_all("div", attrs={"class": "SongRow_container__0d2_U"})
	track_urls = []
	for track in tracks:
		track_urls.append({
			"link": f"{BASE_URL}{track.a['href']}",
			"title": track.find(class_='SongTitle_link__C19Jt'),
			"artist": track.find(class_='Subtitle_subtitle__k3Fvf')
		})
	return track_urls


def get_seasons(url):
	pass


def get_youtube_links(tracks):
	pass


def fetch_links(request_query, content_type, year=None):
	request_query = request_query.replace(" ", "-").lower()
	tracks = []
	if content_type == 'Movie':
		url = f"{BASE_URL}/movie/{request_query}-{year}"
		tracks = get_tracks(url)
	elif content_type == 'Show':
		url = f"{BASE_URL}/show/{request_query}"
		tracks = get_seasons(url)
	if tracks:
		get_youtube_links(tracks)
	else:
		print("Cannot find specified show/movie in tunefind")
