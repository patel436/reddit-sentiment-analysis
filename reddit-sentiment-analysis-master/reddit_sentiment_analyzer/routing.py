
from django.urls import path
from reddit_sentiment_analyzer.consumers import RedditCommentsConsumer


websocket_urlpatterns = [
    path('ws/reddit_comments/', RedditCommentsConsumer.as_asgi()),
]