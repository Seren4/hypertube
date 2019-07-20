from rest_framework import serializers

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import  SocialAccount
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'photo', 'photo_url', 'language', 'login_method', 'user')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, allow_null=True)
    login_method = serializers.SerializerMethodField('get_method')

    class Meta:
        model = User
        read_only_fields = ('login_method',)
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile', 'is_active', 'login_method')

    def get_method(self, obj):
        """ Get the current objects status """
        if SocialAccount.objects.filter(user_id=obj.id).exists():
            b = SocialAccount.objects.filter(user_id=obj.id).latest('last_login')
            return b.provider
        elif Profile.objects.filter(user=obj).exists():
            a = Profile.objects.get(user=obj)
            if a.login_method:
                return a.login_method
            else:
                return "standard"
        return "error"

    def validate_profile(self, profile):
        codes = ['fr', 'en']
        if profile.get('language') in codes:
            return profile
        else:
            raise serializers.ValidationError(
                'Language error'
            )

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            profile.language = profile_data.get('language', profile.language)
            profile.save()
            # print (profile_data, profile)

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance



# RESET PASSWORD EMAIL SEND FORM FIX
from rest_auth.serializers import PasswordResetSerializer
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import UserTokenForm, PasswordResetTokenGenerator


class PasswordSerializer (PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm
    default_token_generator = UserTokenForm