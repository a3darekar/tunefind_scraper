from django.db import models

# Create your models here.


class Movie(models.Model):
	title = models.CharField(max_length=200)
	year = models.PositiveIntegerField()
	tunefind_url = models.URLField(max_length=200)


class Show(models.Model):
	title = models.CharField(max_length=200)
	year = models.IntegerField(blank=True, null=True)
	tunefind_url = models.URLField(max_length=200)


class Season(models.Model):
	number = models.IntegerField()
	show = models.ForeignKey(Show, on_delete=models.CASCADE)
	tunefind_url = models.URLField(max_length=200)


class Episode(models.Model):
	title = models.CharField(max_length=200)
	season = models.ForeignKey(Season, on_delete=models.CASCADE)
	tunefind_url = models.URLField(max_length=200)


class SeriesTracks(models.Model):
	title = models.CharField(max_length=200)
	artist = models.CharField(max_length=200)
	episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
	tunefind_url = models.URLField(max_length=200)
	youtube_url = models.URLField(max_length=200)


class MovieTracks(models.Model):
	title = models.CharField(max_length=200)
	artist = models.CharField(max_length=200)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

	tunefind_url = models.URLField(max_length=200)
	youtube_url = models.URLField(max_length=200)

