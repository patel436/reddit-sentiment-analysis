from django.contrib import admin
from .models import User, Topic, Tweet
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Tweet)
