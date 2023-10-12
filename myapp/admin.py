from django.contrib import admin
from .models import Category, UserProfile, UserImage, Post, Comment

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(UserImage)