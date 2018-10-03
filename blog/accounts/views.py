from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class Signup(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('accounts:login')
  template_name = 'accounts/signup.html'