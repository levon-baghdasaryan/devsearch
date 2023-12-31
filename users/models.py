from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
import uuid


class ProfileManager(models.Manager):
    def search(self, search_query):
        skills = Skill.objects.filter(name__icontains=search_query)
        return self.get_queryset().distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
        )


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True,
                                      upload_to='profiles/',
                                      default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    class Meta:
        ordering = ['created']

    def __str__(self):
        return (self.user.username)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except Exception:
            url = ''
        return url


class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,
                              null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                               null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models. EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
