from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)


    def save(self, *args, **kwargs):
        #extract the video id from youtube url
        #if not self.url.startswith('https://www.youtube.com/watch'):
            #raise ValidationError(f'Not a YouTube URL {self.url}')
        url_components = parse.urlparse(self.url)

        if url_components.scheme != 'https':
            raise ValidationError(f'Not a YouTube URL {self.url}')

        if url_components.scheme != 'www.youtube.com':
            raise ValidationError(f'Not a YouTube URL {self.url}')

        if url_components.scheme != '/watch':
            raise ValidationError(f'Not a YouTube URL {self.url}')

        query_string = url_components.query
        if not query_string:
            raise ValidationError(f'Invalid YouTube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True)
        v_parameters_list = parameters.get('v')
        if not v_parameters_list: #check if none or empty list
            raise ValidationError(f'Invalid YouTube URL, missing parameters {self.url} ')
        self.video_id = v_parameters_list[0] #string

        super().save(*args, **kwargs)

    def __str__(self):
        return f'ID: {self.pk}, Name:{self.name}, URL: {self.url},Video ID: {self.video_id}, Notes: {self.notes[:200]}'