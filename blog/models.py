from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Blog(models.Model):
    OPTIONS = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
  
    title = models.CharField(max_length=100)    
    content = models.TextField()
    image = models.URLField(blank=True, default="https://i.picsum.photos/id/1066/400/300.jpg?hmac=KsSGWNXje7B9dXUx6O6QzUlD4m4NzUQkkUzoVk4xmHk")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, related_name="post_user", on_delete=models.PROTECT, default='Anonymous User') bu da olabilir 
    status = models.CharField(max_length=10, choices=OPTIONS, default='d')
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def comment_count(self):
        return self.comment_set.all().count()
    
    def view_count(self):
        return self.postview_set.all().count()
    
    def like_count(self):
        return self.like_set.all()
    
    def comments(self):
        return self.comment_set.all()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return self.user.username
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    