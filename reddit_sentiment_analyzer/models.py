from django.db import models

# Create your models here.

class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255, unique=True)
    twitter_handle = models.CharField(max_length=255)
    posting_date = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.tweet_id
class Topic(models.Model):
    topic_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"topic {self.topic_name} is created at {self.created_at} and is {'Active' if self.active else 'not active'}"
