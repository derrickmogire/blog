from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save
# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    author = models.ForeignKey(
        User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, verbose_name=(
        "like"), related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=True)
    favourite = models.ManyToManyField(
        User, verbose_name=("favourite"), related_name='favourite')
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("details", kwargs={"id": self.id, "slug": self.slug})

    def snippet(self):
        return self.body[:15] + '...'

    def total_likes(self):
        return self.likes.count()


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=(
        "Profile"), on_delete=models.CASCADE)
    dob = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    dp = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "profile of user {}".format(self.user.username)


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images/', null=True)

    def __str__(self):
        return self.post.title + 'image'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    user = models.ForeignKey(User, verbose_name=(
        "user"), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey("self", verbose_name=(
        "reply"), related_name='replies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(str(self.post.title), str(self.user.username))
