from django.db import models

# Create your models here.

class Tweet(models.Model):
    topic_name = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    posting_date = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.tweet_id
    
class LoginUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

class Topic(models.Model):
    topic_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"topic {self.topic_name} is created at {self.created_at} and is {'Active' if self.active else 'not active'}"
