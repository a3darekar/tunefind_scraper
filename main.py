import sys

if __name__ == '__main__':
	while True:
		print("Select Content Type:\n 1. Movie\n 2. TV Show\n")
		content_type = input("Select Content type:")

		if content_type == '1':
			print("Enter name of the movie:")
		elif content_type == '2':
			print("Enter name of the series:")
		else:
			print("Select right option.")

		request_query = input()
		print(f"Looking for music from {request_query}")
		# @TODO: Initialize Scraper
		sys.exit(0)
