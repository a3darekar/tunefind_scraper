import sys

from tunefind_scraper import fetch_links, content_types

if __name__ == '__main__':
	while True:
		try:
			print("Select Content Type:\n")
			for key, content_type in content_types.items():
				print(f"{key}. {content_type}")
			content_type = int(input("Select Content type:"))

			if content_type == 1:
				request_query = input("Enter name of the movie:")
				release_year = int(input("Enter Year it was released:"))
				fetch_links(request_query, content_types[content_type], release_year)
			elif content_type == 2:
				print("Enter name of the series:")
				print(f"Looking for music from {request_query}")
				fetch_links(request_query, content_types[content_type])
			else:
				print("Select right option.")

			# @TODO: Initialize Scraper
			break
		except ValueError as v:
			print("Enter valid info")
	sys.exit(0)
