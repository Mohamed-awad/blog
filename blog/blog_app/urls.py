from django.conf.urls import url, re_path
from django.urls import path
from . import views
from .feeds import PostFeed

app_name = 'blog'

urlpatterns = [
  url(r'^$', views.post_list, name='post_list'),
  url(r'^add_post/$', views.add_post, name='add_post'),
  url(r'^(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
  url(r'^api/$', views.PostList.as_view(), name='list_post_api'),
  url(r'^api/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='detail_post_api'),
  url(r'^feed/$', PostFeed(), name='post_feed'),
  url(r'^like_post/(?P<pk>\d+)$', views.like_post, name='like_post'),
  url(r'^del_post/(?P<pk>\d+)$', views.del_post, name='del_post'),
  url(r'^update_post/(?P<pk>\d+)$', views.UpdatePost.as_view(), name='update_post'),
]
