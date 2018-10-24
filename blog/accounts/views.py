from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.blog_app.models import Post, Like
from django.shortcuts import render


class UserList(LoginRequiredMixin, generics.ListCreateAPIView):
  login_url = 'accounts:login'
  queryset = User.objects.all()
  serializer_class = UserSerializer


class UserDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
  login_url = 'accounts:login'
  queryset = User.objects.all()
  serializer_class = UserSerializer


class Signup(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('accounts:login')
  template_name = 'accounts/signup.html'


@login_required
def get_user_profile(request):
  user = request.user
  user_posts = Post.objects.filter(author=user)
  context = {
    'user': user,
    'posts': user_posts,
  }
  return render(request, 'accounts/profile.html', context)


@login_required
def get_liked_posts(request):
  user = request.user
  liked_posts = Like.objects.filter(user=user, value=True)
  posts = list()
  for liked_post in liked_posts:
    posts.append(liked_post.post)
  posts_1 = Post.objects.filter(title__in=posts)
  context = {
    'user': user,
    'posts': posts_1,
  }
  return render(request, 'accounts/profile.html', context)