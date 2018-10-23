from django.contrib.auth.forms import UserCreationForm
# from .forms import UserProfileForm
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.blog_app.models import Post
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
    'user_posts': user_posts,
  }
  return render(request, 'accounts/profile.html', context)