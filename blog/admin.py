
from django.contrib import admin

from .models import Blog, Category, Comment, Like, PostView

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(PostView)