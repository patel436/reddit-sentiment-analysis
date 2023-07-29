from django.apps import AppConfig

import os

class RedditSentimentAnalyzerConfig(AppConfig):
    name = 'reddit_sentiment_analyzer'


    def ready(self):
        from reddit_sentiment_analyzer.views import restart_all_workers
        if os.environ.get('RUN_MAIN'):
            restart_all_workers()