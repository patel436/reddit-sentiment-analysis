from django.urls import path
from reddit_sentiment_analyzer import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('user_home/', views.user_home, name="user_home"),
    path('brand_list/', views.get_brandlist, name="brand_list"),
    path('chart/<str:brand>/', views.show, name='chart')
]