from django.conf.urls import url
from . import views
from .feeds import PostFeed

app_name = 'blog'

urlpatterns = [
  url(r'^$', views.post_list, name='post_list'),
  url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
  url(r'^api/$', views.PostList.as_view(), name='list_post_api'),
  url(r'^api/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='detail_post_api'),
  url(r'^feed/$', PostFeed(), name='post_feed'),
]
