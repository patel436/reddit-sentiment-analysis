from django.contrib import admin
from .models import LoginUser, Topic, Tweet
# Register your models here.

admin.site.register(LoginUser)
admin.site.register(Topic)
admin.site.register(Tweet)
