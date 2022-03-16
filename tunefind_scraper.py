import re

import requests as requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tunefind.com"

content_types = {
	1: "Movie",
	2: "Show"
}


def get_tracks(url):
	pass


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
