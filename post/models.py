from django.db import models
from django.urls import reverse
from userprofile.models import Doctor
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    post_content = models.TextField()
    image = models.ImageField(null=True, blank=True, height_field="height", width_field="width")
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, blank=False, null=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Posts/Dicussions"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    @classmethod
    def list_posts(cls):
        return cls.objects.all()


class Photo(models.Model):
    image = models.ImageField(upload_to="posts", height_field=None, width_field=None)
    post = models.ForeignKey(Post, default=None)
    doctor = models.ForeignKey(Doctor)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class Comment(models.Model):
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    post = models.ForeignKey(Post)
    doctor = models.ForeignKey(Doctor)


class Reply(models.Model):
    reply_content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    parent_comment_id = models.ForeignKey(Comment)
    post = models.ForeignKey(Post)
    doctor = models.ForeignKey(Doctor)




