from django.shortcuts import render
from .forms import LoginForm, RegisterForm, CreateTopicForm
from .models import Topic
from datetime import datetime
from reddit_sentiment_analyzer.redditUtils import RedditHandle
from reddit_sentiment_analyzer.utils import ThreadPool, THREADPOOL_LIMIT, SingletonQueue
from reddit_sentiment_analyzer.workers import create_worker
from reddit_sentiment_analyzer.redditUtils import start_fetching_comments, start_fetching_submissions

# Create your views here.
def index(request):
    login_form = LoginForm()
    return render(request, 'index.html', {'login_form' : login_form})

def about(request):
    return render(request, 'about.html')

def user_home(request):
    create_topic_form = CreateTopicForm()
    return render(request, 'user_home.html', {'create_topic_form' : create_topic_form})
def register(request):
    register_form = RegisterForm()
    return render(request, 'register.html', {'register_form' : register_form})

def show(request, brand):
    rutils = RedditHandle()
    tweets = rutils.get_tweets(brand)
    positive_tweets = [tweet for tweet in tweets if tweet['compound'] > 0.2]
    negative_tweets = [tweet for tweet in tweets if tweet['compound'] < -0.2]
    neutral_tweets = [tweet for tweet in tweets if tweet['compound'] == 0]
    total_tweets = len(tweets)
    positive_sentiment = int((len(positive_tweets) / total_tweets) * 100)
    negative_sentiment = int((len(negative_tweets) / total_tweets) * 100)
    neutral_sentiment = int(100 - (positive_sentiment + negative_sentiment))

    context = {}
    context['sentiment'] = {
        'positive_sentiment': positive_sentiment,
        'negative_sentiment': negative_sentiment,
        'neutral_sentiment': neutral_sentiment
    }
    context['positive_tweets'] = positive_tweets[:5]
    context['negative_tweets'] = negative_tweets[:5]
    context['neutral_tweets'] = neutral_tweets[:5]

    return render(request, 'chart.html', context)

def get_brandlist(request):
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            topic_name = form.cleaned_data["topicname"]
            create_topic(topic_name)
    topics = Topic.objects.all()
    return render(request, 'brand_list.html', context={'topics': topics})

def get_topics(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic_name')
        create_topic(topic_name)
    topics = Topic.objects.all()
    return render(request, 'topics.html', context={'topics': topics})

def create_topic(topic_name):
    try:
        t = Topic(topic_name=topic_name, created_at=datetime.now(), active=True)
        t.save()
    except Exception as e:
        print(e)
    restart_all_workers()

def restart_all_workers():
    t = ThreadPool()
    q = SingletonQueue()
    t.destroy_all_threads()

    topics = [topic.topic_name.lower() for topic in Topic.objects.all() if topic.active]

    # starting streaming submissions and comments
    t.execute(start_fetching_comments, topics, q)
    t.execute(start_fetching_submissions, topics, q)

    # starting worker nodes
    for _ in range(THREADPOOL_LIMIT):
        t.execute(create_worker, q)
