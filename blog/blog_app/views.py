from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class PostList(LoginRequiredMixin, generics.ListCreateAPIView):
  login_url = 'accounts:login'
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
  login_url = 'accounts:login'
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class AddPost(LoginRequiredMixin, CreateView):
  def get_initial(self):
    return {
      'author': self.request.user
    }

  def set(self):
    return {
      'author': self.request.user
    }
  login_url = 'accounts:login'
  form_class = PostCreateForm
  template_name = 'blog/post/create.html'
  success_url = reverse_lazy('blog:post_list')
  http_method_names = ('post', 'get', 'set')


def post_list(request):
  list_objects = Post.published.all()
  paginator = Paginator(list_objects, 3)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)
  return render(request, 'blog/post/list.html', {'posts': posts})


@login_required
def post_detail(request, year, month, day, post):
  post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
  return render(request, 'blog/post/detail.html', {'post': post})
