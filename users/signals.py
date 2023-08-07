from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Profile
from .emails import register_user_email


def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name
        )

        register_user_email(profile, settings.EMAIL_HOST_USER)


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except Exception:
        pass


post_save.connect(createProfile, sender=get_user_model())
post_save.connect(updateUser, sender=Profile)
# Deletes the corresponding user when a profile gets deleted
post_delete.connect(deleteUser, sender=Profile)
