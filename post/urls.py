from django.conf.urls import url
from post import views as post_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^post/$', login_required(post_views.PostCreate.as_view()), name='Post'),
    url(r'^post/detail/(?P<pk>[0-9]+)/$', login_required(post_views.PostDetail.as_view()), name='post-detail'),
    url(r'^feed/$', login_required(post_views.Posts.as_view()), name='posts'),
    url(r'^discussions/$', login_required(post_views.PostList.as_view()), name='all-discussions'),
    url(r'comment/(?P<pk>[0-9]+)/$', post_views.add_comment_to_post,  name='comment'),
    url(r'post/comment/(?P<pk>[0-9]+)/$', post_views.post_comment_add_view,  name='post-comment'),
    # url(r'post/(?P<pk>[0-9]+)/image/$', post_views.add_image_on_post,  name='post-image'),
]
