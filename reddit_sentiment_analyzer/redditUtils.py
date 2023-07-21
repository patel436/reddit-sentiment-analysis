from textblob import TextBlob
import praw
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

class RedditHandle():
    def get_tweets(self, query, count=1000):

        # self.cf = ConfigReader()
        # client_id = self.cf.get('REDDIT', 'client_id')
        # client_secret = self.cf.get('REDDIT', 'client_secret')
        try:
            user_agent = "Scraper 1.0 by /u/patel436"
            reddit = praw.Reddit(
                client_id="0mq-q69XrM1ENsI9bQov-A",
                client_secret="qMCLIIzvj-6AcXIWbzUYrkZiciR9Mg",
                user_agent=user_agent
            )
            print('Authenticated')
        except:
            print("Sorry! Error in authentication!")

        headlines = set()
        for submission in reddit.subreddit(query).top(limit=count):
                headlines.add(submission.title)
                print(submission.title)
                print(submission.author)

        sia = SIA()
        results = []
        for line in headlines:
            pol_score = sia.polarity_scores(line)
            pol_score['headline'] = line
            results.append(pol_score)
        return results

def authenticate():
    try:
        user_agent = "Scraper 1.0 by /u/patel436"
        reddit = praw.Reddit(
            client_id="0mq-q69XrM1ENsI9bQov-A",
            client_secret="qMCLIIzvj-6AcXIWbzUYrkZiciR9Mg",
            user_agent=user_agent
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
                q.enqueue((topic_name, (submission.author, submission.title, submission.created_utc)))


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
                q.enqueue((topic_name, (comment.author, comment.body, comment.created_utc)))

