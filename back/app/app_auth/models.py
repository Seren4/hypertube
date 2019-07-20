from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from allauth.account.signals import email_confirmed
from allauth.account.models import EmailAddress

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)
    photo_url = models.URLField(null=True, blank=True)
    language = models.CharField(default='en', max_length=2)
    login_method = models.CharField(null=True, max_length=10)


# ---> create profile instance on user create
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # Once the email address is confirmed, make new email_address primary.
    # This also sets user.email to the new email address.
    # email_address is an instance of allauth.account.models.EmailAddress
    email_address.set_as_primary()
    # Get rid of old email addresses
    stale_addresses = EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()

