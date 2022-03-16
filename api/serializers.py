from rest_framework import serializers
from api.models import Movie, MovieTracks, Show, Season, Episode, SeriesTracks


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'tunefind_url']


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['id', 'title', 'tunefind_url']


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['number', 'show', 'tunefind_url']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'season', 'tunefind_url']


class SeriesTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesTracks
        fields = ['title', 'artist', 'episode', 'tunefind_url', 'youtube_url']


class MovieTracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieTracks
        fields = ['title', 'artist', 'movie', 'tunefind_url', 'youtube_url']



