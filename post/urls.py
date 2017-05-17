from django.conf.urls import url
from post import views as post_views

urlpatterns = [
    url(r'^post/$', post_views.PostCreate.as_view(), name='Post'),
    #url(r'^feed/$', post_views.post_list, name='feed'),
    url(r'^feed/$', post_views.PostList.as_view(), name='all-posts'),
]