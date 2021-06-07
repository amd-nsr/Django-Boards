from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

class Board(models.Model):
    name = models.CharField(max_length=30)
    descrption = models.CharField(max_length=100)
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()
    
    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.CharField(max_length=30)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey('Board', related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True , related_name='+', on_delete=models.CASCADE)
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
