from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm, CreateTopicForm
from .models import Topic, Tweet, LoginUser
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from reddit_sentiment_analyzer.redditUtils import get_tweets, get_compound
from reddit_sentiment_analyzer.utils import ThreadPool, THREADPOOL_LIMIT, SingletonQueue
from reddit_sentiment_analyzer.workers import create_worker
from reddit_sentiment_analyzer.redditUtils import start_fetching_comments, start_fetching_submissions
from django.utils import timezone
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
from django.db.models import F, ExpressionWrapper, FloatField, Func
from statistics import mean

# Create your views here.
def index(request):
    login_form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('reddit_sentiment_analyzer:user_home')  
        else:
                msg = "Invalid username or password."
                return render(request, 'login.html', {'login_form' : login_form, 'msg' : msg})

    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'login_form' : login_form})

def about(request):
    return render(request, 'about.html')

def user_logout(request):
    logout(request)
    return redirect('reddit_sentiment_analyzer:index')

@login_required
def user_home(request):
    create_topic_form = CreateTopicForm()
    return render(request, 'user_home.html', {'create_topic_form' : create_topic_form})

def register(request):
        register_form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('reddit_sentiment_analyzer:index')  # Redirect on successful registration
            
            else:
                msg = "Please enter the Correct Data"
                return render(request, 'register.html', {'register_form' : register_form, 'msg' : msg})
        else:
            form = RegisterForm()
            return render(request, 'register.html', {'register_form' : register_form})

@login_required
def show(request, brand):
    tweets = get_tweets(brand)
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

    q = SingletonQueue()
    q.stream = True
    return render(request, 'chart.html', context)

@login_required
def get_brandlist(request):
    msg = ''
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            topic_name = form.cleaned_data["topicname"]
            if Topic.objects.all().count() < 3:
                create_topic(topic_name)
            else:
                msg = 'Upto 3 brands allowed. Upgrade to premium for more!'
    topics = Topic.objects.all()
    return render(request, 'brand_list.html', context={'topics': topics, 'msg' : msg})


def get_topics_list():
    topic_list = Topic.objects.all()
    return topic_list

@login_required
def get_trendline(request):
    generate_trendline(request, '')

@login_required
def generate_trendline(request, topic_name=''):
    print("topic_name is ", topic_name)
    options = get_topics_list()
    if topic_name:
        # chart call here
        context = {
            "options": options,
            "selected_option": topic_name,
            "trendline_data": {
                "daily": get_aggregated_data('daily', topic_name),
                "monthly": get_aggregated_data('monthly', topic_name),
                "yearly": get_aggregated_data('yearly', topic_name),
            }
        }
        print(context)
        return render(request, 'trendline.html', context=context)

    return render(request, 'trendline.html', context={"options": options})


def get_aggregated_data(frequency,topic_name):
    # Get the current date
    current_date = timezone.now()

    # Calculate the start date based on the specified frequency
    if frequency == "daily":
        start_date = current_date - relativedelta(days=30)
        date_format = "%b %d, %Y"  # Format for daily labels: "Jun 15, 2023"
    elif frequency == "monthly":
        start_date = current_date - relativedelta(months=12)
        date_format = "%b %Y"  # Format for monthly labels: "Jun 2023"
    elif frequency == "yearly":
        start_date = current_date - relativedelta(years=5)
        date_format = "%Y"  # Format for yearly labels: "2023"
    else:
        raise ValueError("Invalid frequency. Supported frequencies are 'daily', 'monthly', and 'yearly'.")

    # Get all tweet records within the specified timeframe
    tweets = Tweet.objects.filter(posting_date__gte=start_date).filter(topic_name=topic_name.lower())

    tweets = get_compound(tweets)

    tweets.sort(key=lambda tweet: tweet.posting_date)

    result = {}
    current_key = None
    compound_values = []
    for tweet in tweets:
        if tweet.posting_date.strftime(date_format) == current_key:
            compound_values.append(tweet.compound)
        else:
            if current_key is not None:
                result[current_key] = mean(compound_values)
            compound_values = [tweet.compound]
            current_key = tweet.posting_date.strftime(date_format)
    else:
        result[current_key] = mean(compound_values)

    op = {
        'labels':[],
        'data':[]
    }

    for key in result.keys():
        op['labels'].append(key)
        op['data'].append(result[key])

    return op

# def get_topics(request):
#     if request.method == 'POST':
#         topic_name = request.POST.get('topic_name')
#         create_topic(topic_name)
#     topics = Topic.objects.all()
#     return render(request, 'topics.html', context={'topics': topics})

def pause_topic(request, topic_name):
    try:
        topic = Topic.objects.get(topic_name=topic_name)
        topic.active = not topic.active
        topic.save()
        restart_all_workers()
    except Exception as e:
        print("Topic does not exist")
    return HttpResponseRedirect(reverse('reddit_sentiment_analyzer:brand_list'))

def delete_topic(request, topic_name):
    try:
        Topic.objects.get(topic_name=topic_name).delete()
    except Exception as e:
        print("failed to delete topic")
    try:
        Tweet.objects.filter(topic_name=topic_name.lower()).delete()
    except Exception as e:
        print("failed to delete tweets")
    restart_all_workers()
    return HttpResponseRedirect(reverse('reddit_sentiment_analyzer:brand_list'))


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
