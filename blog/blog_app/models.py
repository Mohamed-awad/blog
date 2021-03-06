from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# custom manager
class PublishedManager(models.Manager):
  def get_queryset(self):
    return super(PublishedManager, self).get_queryset().filter(status='published')


# Post Model
class Post(models.Model):
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
  )

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique_for_date='publish')
  author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
  body = models.TextField()
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
  image = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True)
  likes = models.IntegerField(default=0)
  dislikes = models.IntegerField(default=0)
  # the default manager
  objects = models.Manager()

  # custom mode manager
  published = PublishedManager()

  class Meta:
    ordering = ('-publish',)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('blog:post_detail', args=[self.pk])


class Like(models.Model):
  user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)
  post = models.ForeignKey(Post, related_name='liked_posts', on_delete=models.CASCADE)
  value = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.user) + ':' + str(self.post) + ':' + str(self.value)
