from textblob import TextBlob
import praw
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from .api_keys import reddit_client_id, reddit_client_secret, reddit_user_agent
from reddit_sentiment_analyzer.models import Tweet
from datetime import datetime

class RedditHandle():

    def get_tweets(self, query, count=1000):
        tweets = Tweet.objects.filter(topic_name=query.lower()).order_by("posting_date").reverse()[:1000]

        sia = SIA()
        results = []
        for tweet in tweets:
            pol_score = sia.polarity_scores(tweet.message)
            tweet.compound = pol_score.get("compound")
            results.append({
                "topic_name": tweet.topic_name,
                "twitter_handle": tweet.twitter_handle,
                "posting_date": tweet.posting_date,
                "message": tweet.message,
                "compound": pol_score.get("compound")
            })
        return results



def authenticate():
    try:
        reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent
        )
        print("Authenticated")
        return reddit
    except:
        return None


def start_fetching_submissions(stop_event, topic_names, q):
    reddit = authenticate()
    if not reddit:
        return
    subreddit = reddit.subreddit("all")
    for submission in subreddit.stream.submissions():
        if stop_event.is_set():
            break
        for topic_name in topic_names:
            if topic_name in submission.title.lower():
                print(submission.title)
                q.enqueue((topic_name, submission.author, submission.title, datetime.fromtimestamp(submission.created_utc)))


def start_fetching_comments(stop_event, topic_names, q):
    reddit = authenticate()
    if not reddit:
        return
    subreddit = reddit.subreddit("all")
    for comment in subreddit.stream.comments():
        if stop_event.is_set():
            break
        for topic_name in topic_names:
            if topic_name in comment.body.lower():
                q.enqueue((topic_name, comment.author, comment.body, datetime.fromtimestamp(comment.created_utc)))

