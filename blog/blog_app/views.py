from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Like
from .serializers import PostSerializer
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView


class PostList(LoginRequiredMixin, generics.ListCreateAPIView):
  login_url = 'accounts:login'
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
  login_url = 'accounts:login'
  queryset = Post.objects.all()
  serializer_class = PostSerializer


@login_required
def add_post(request):
  if request.method == 'POST':
    post_form = PostCreateForm(request.POST, request.FILES)
    if post_form.is_valid():
      post = post_form.save(commit=False)
      post.author = request.user
      post.save()
      return HttpResponseRedirect(reverse_lazy('blog:post_list'))
  elif request.method == 'GET':
    form = PostCreateForm()
    context = {
      'form': form,
    }
    return render(request, 'blog/post/create.html', context)


@login_required
def del_post(request, pk):
  post = Post.objects.get(id=pk)
  if request.user == post.author:
    post.delete()
  return HttpResponseRedirect(reverse_lazy('blog:post_list'))


class UpdatePost(LoginRequiredMixin, UpdateView):
  form_class = PostCreateForm
  template_name = 'blog/post/create.html'

  def get_object(self, queryset=None):
    obj, created = Post.objects.get_or_create(id=self.kwargs['pk'])
    return obj


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
def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk, status='published')
  like = Like.objects.filter(user=request.user, post=post)
  flag = False
  if like:
    flag = True
  context = {
    'flag': flag,
    'post': post,
  }
  return render(request, 'blog/post/detail.html', context)


@login_required
def like_post(request, pk):
  user = request.user
  post = Post.objects.get(id=pk)
  post.likes = post.likes + 1
  like = Like.objects.get_or_create(user=user, post=post, value=True)
  return HttpResponseRedirect(reverse_lazy('blog:post_detail', kwargs={'pk': pk}))


@login_required
def share_post(request, pk):
  post = Post.objects.get(id=pk)
  post.author = request.user
  post1 = Post(title=post.title, body=post.body,
               author=request.user, image=post.image)
  post1.save()
  return HttpResponseRedirect(reverse_lazy('blog:post_detail', kwargs={'pk': post1.pk}))
