from django.urls import path
from reddit_sentiment_analyzer import views

app_name='reddit_sentiment_analyzer'

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('user_home/', views.user_home, name="user_home"),
    path('brand_list/', views.get_brandlist, name="brand_list"),
    path('chart/<str:brand>/', views.show, name='chart'),
    path('pause_topic/<str:topic_name>/', views.pause_topic, name='pause_topic'),
    path('delete_topic/<str:topic_name>/', views.delete_topic, name='delete_topic'),
    path(r'trendline/', views.generate_trendline, name="trendline"),
    path(r'trendline/<str:topic_name>/', views.generate_trendline, name="trendline")
]