from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import SocialToken
import requests
from django.shortcuts import redirect

from rest_framework_jwt.settings import api_settings

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


# from project/users/allauth.py:
class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        if request.user:
            payload = jwt_payload_handler(request.user)
            token = jwt_encode_handler(payload)
            path = "http://localhost:3000/login?jwt={access_token}"
            path_format = path.format(access_token=token)
            return path_format
        return 'http://localhost:3000/login'


    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        user = super().save_user(request, user, form, False)
        user_field(user, 'first_name', request.data.get('first_name', ''))
        user_field(user, 'last_name', request.data.get('last_name', ''))
        user.save()

        a = Profile.objects.get(user=user)
        a.photo = request.data.get('photo', '')
        a.save()
        return user


from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)



from django.dispatch import Signal, receiver
from allauth.account.signals import user_signed_up, user_logged_in
from .models import Profile


# FROM ---> https://stackoverflow.com/questions/29082098/django-allauth-retrieve-avatar-profile-pictures
@receiver(user_signed_up)
def social_login_profilepic(*args, **kwargs):
    sociallogin = kwargs.get('sociallogin', None)
    user = kwargs.get('user', None)
    if sociallogin is not None:
        picture_url = None
        if sociallogin.account.provider == 'google':
            picture_url = sociallogin.account.extra_data['picture']

        if sociallogin.account.provider == 'github':
            picture_url = sociallogin.account.extra_data['avatar_url']

        Profile.objects.get(user__id=user.id).delete()
        profile = Profile(user=user, photo_url=picture_url)
        profile.save()

