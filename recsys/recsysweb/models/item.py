from django.db import models
from taggit.managers import TaggableManager


class Item(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.TextField(max_length = 500,  verbose_name = 'Name')
    description = models.TextField(max_length = 5000, verbose_name = 'Description')
    image       = models.TextField(max_length = 500,  verbose_name = 'Image URL')
    popularity  = models.FloatField(default   = 0,    verbose_name = 'Popularity')
    rating      = models.FloatField(default   = 0,    verbose_name = 'Rating')
    votes       = models.FloatField(default   = 0,    verbose_name = 'Votes')
    tags        = TaggableManager()

    class Meta:
        indexes = [
            models.Index(fields=['popularity'])
        ]

    def __str__(self):
        return self.name

