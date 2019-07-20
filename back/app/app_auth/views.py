from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from .models import *
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
import requests, json


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

### USER VIEW

from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import FileUploadParser

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.socialaccount.models import  SocialAccount
from .permissions import IsOwner, IsPhotoOwner


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def create(self, request):
        return Response({'success': False})

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)

    @action(detail=False, methods=['GET'], name='Get user data')
    def get_user(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], name='Edit user profile')
    def edit_profile(self, request):
        if not request.data:
            return Response({"success": False})
        for i, j in request.data.items():
            if not j:
                return Response({"success": False, "message": {"error": {"Please fill all the fields"}} })

        # check the login method
        if Profile.objects.filter(user=request.user).exists():
            profile = Profile.objects.get(user=request.user)
            if SocialAccount.objects.filter(user_id=request.user.id).exists() or profile.login_method == "42":
                for i, j in request.data.items():
                    if i != 'profile.language':
                        return Response({"success": False, "message": {"error": {"You are not allowed"}}})

            headers = {"Authorization": request.META["HTTP_AUTHORIZATION"]}
            url = 'http://localhost:8000/auth/user/' + str(request.user.id) + '/'
            resp = requests.patch(url, data=request.data, headers=headers)
            content = json.loads(resp.content.decode("utf-8"))
            if resp and User.objects.filter(pk=request.user.id).exists():
                user_obj = User.objects.get(pk=request.user.id)
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                if 'email' in request.data:
                    email = request.data['email']
                    # ----> the email remains unchanged until the user validates it. (see update_user_email in models)
                    EmailAddress.objects.add_email(request, request.user, email, confirm=True)
                    return Response({"success": True, "token": token, 'message': 'Please check your mail to confirm the new mail'})
                return Response({"success": True, "token": token})
            return Response({"success": False, "message": content})
        return Response({"success": False})

    @action(detail=False, methods=['POST'], name='Edit user profile')
    def edit_password(self, request):
        if not request.data:
            return Response({"success": False})
        url = 'http://localhost:8000/auth/rest-auth/password/change/'
        headers = {
            "Authorization": request.META["HTTP_AUTHORIZATION"]
        }
        resp = requests.post(url, data=request.data, headers=headers)
        # print(resp.content)
        if resp and User.objects.filter(pk=request.user.id).exists():
            user_obj = User.objects.get(pk=request.user.id)
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            return Response({"success": True, "token": token})
        content = json.loads(resp.content.decode("utf-8"))
        return Response({"success": False, "message": content})


###       PHOTO VIEW
class PhotoUploadView(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_class = (FileUploadParser,)
    permission_classes = (IsPhotoOwner,IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user__id=user.pk)

    def create(self, request):
        return Response({'success': False})

    def update(self, request, *args, **kwargs):
        if not request.data:
            return Response({"success": False})
        # print ("----------> photo", request.data['photo'])
        instance = self.get_object()
        serializer = ProfileSerializer(
            instance=instance,
            data=request.data
        )
        if serializer.is_valid(raise_exception=False):
            if request.data['photo'].content_type == 'image/tiff':
                return Response({"success": False, "message": 'wrong format'})
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})

import re

class RequestsView(viewsets.ViewSet):

    permission_classes = (AllowAny,)
    authentication_classes = []

    @action(detail=False, methods=['post'])
    def signin(self, request):
        if not all(k in request.data for k in
                   ("username", "password")):
            return Response({'success': False, 'errors': "please fill all the fields"})
        body = request.data
        test1 = re.search("^([a-zA-Z0-9]){6,12}$", body['username'])
        test2 = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*])[A-Za-z\\d!@#$%^&*]{8,20}$",  body['password'])
        if test1 is None or test2 is None:
            return Response({'success': False, 'message': 'Validation error'})
        user = authenticate(username=body['username'], password=body['password'])
        if user is not None:
            resp = requests.post('http://localhost:8000/auth/rest-auth/login/', data={
                'username': body['username'],
                'password': body['password'],
            })
            if resp:
                body_unicode = resp.content.decode('utf-8')
                body = json.loads(body_unicode)
                return Response({'success': True, 'token': body['token'], 'user': body['user']})
            return Response({'success': False})
        else:
            return Response({'success': False})


    @action(detail=False, methods=['post'])
    def signup(self, request):
        if not all(k in request.data for k in ("photo", "username", "email", "first_name", "last_name", "password1", "password2")):
            return Response({'success': False, 'errors': "please fill all the fields"})
        if not request.data['photo']:
            return Response({'success': False, 'errors': "photo error"})
        resp = requests.post('http://localhost:8000/auth/rest-auth/registration/', data={
            'username': request.data['username'],
            'email': request.data['email'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'password1': request.data['password1'],
            'password2': request.data['password2'],
        }, files={'photo': request.data['photo']})
        if resp:
            content = json.loads(resp.content.decode('utf-8'))
            if content['detail'] and content['detail'] == 'Verification e-mail sent.':
                return Response({'success': True, 'message': content['detail']})
        return Response({'success': False, 'errors': resp.content})

    @action(detail=False, methods=['post'])
    def login42(self, request):
        if not request.data or 'state' not in request.data or 'code' not in request.data:
            return Response({'success': False})
        body = request.data
        if body['state'] == '42state':
            r = requests.post('https://api.intra.42.fr/oauth/token', data={
                'grant_type': 'authorization_code',
                'client_id': '',
                'client_secret': '',
                'code': body['code'],
                'state': body['state'],
                'redirect_uri': 'http://localhost:3000/login'
            })
            if r:
                body_unicode = r.content.decode('utf-8')
                body = json.loads(body_unicode)
                headers = {"Authorization": "Bearer " + body['access_token']}
                r2 = requests.get('https://api.intra.42.fr/v2/me', data='Null', headers=headers).json()
                if r2:
                    ### create User ###
                    # print(r2)
                    check = User.objects.filter(username=r2['login'], email=r2['email']).exists()
                    username = User.objects.filter(username=r2['login']).exists()
                    email = User.objects.filter(email=r2['email']).exists()
                    if not check and not email and not username:
                        user = User.objects.create_user(username=r2['login'], email=r2['email'])
                        user.first_name = r2['first_name']
                        user.last_name = r2['last_name']
                        user.profile.photo_url = r2['image_url']
                        user.profile.login_method = "42"
                        user.save()
                        payload = jwt_payload_handler(user)
                    elif username and not email:
                        count = User.objects.all().count()
                        username = r2['login'] + str(count)
                        user = User.objects.create_user(username=username, email=r2['email'])
                        user.first_name = r2['first_name']
                        user.last_name = r2['last_name']
                        user.profile.photo_url = r2['image_url']
                        user.profile.login_method = "42"
                        user.save()
                        payload = jwt_payload_handler(user)
                    elif email and not username:
                        user = User.objects.get(email=r2['email'])
                        payload = jwt_payload_handler(user)
                    else:
                        user = User.objects.get(email=r2['email'])
                        payload = jwt_payload_handler(user)
                    serializer = UserSerializer(user)
                    token = jwt_encode_handler(payload)
                    return Response({'success': True, 'token': token, 'user': serializer.data})
        return Response({'success': False})

    @action(detail=False, methods=['post'], url_path='token-verify')
    def token_verify(self, request):
        if not request.data or "token" not in request.data:
            return Response({'success': False})
        body = request.data
        resp = requests.post('http://localhost:8000/auth/api-token-verify/', data={
            'token': body['token'],
        })
        body_unicode = resp.content.decode('utf-8')
        body = json.loads(body_unicode)
        if 'token' in body:
            return Response({'success': True})
        else:
            return Response({'success': False})

    @action(detail=False, methods=['post'], url_path='token-refresh')
    def token_refresh(self, request):
        if not request.data or "token" not in request.data:
            return Response({'success': False})
        body = request.data
        resp = requests.post('http://localhost:8000/auth/api-token-refresh/', data={
            'token': body['token'],
        })
        body_unicode = resp.content.decode('utf-8')
        body = json.loads(body_unicode)
        if 'token' in body:
            return Response({'success': True, 'token': body['token']})
        else:
            return Response({'success': False})

    @action(detail=False, methods=['get'], url_path='verify-email/(?P<token>[^/.]+)')
    def verify_email(self, request, token):
        try:
            email = EmailConfirmation.objects.get(key=token)
        # no confimation link has been sent => fake link
        except EmailConfirmation.DoesNotExist:
            email = None

        # link has been sent and is valid
        if email is not None:
            verified = EmailAddress.objects.get(email=email.email_address.email)
            valid_link = verified.verified == False
            if valid_link:
                requests.get('http://localhost:8000/accounts/confirm-email/' + token + '/')
            # link has been already used

        # no confimation link has been sent => fake link
        else:
            valid_link = False
        # print (valid_link)
        redirect_url = 'http://localhost:3000/login?confirmed=' + str(valid_link)
        return HttpResponseRedirect(redirect_to=redirect_url)

    @action(detail=False, methods=['post'], url_path='password_reset')
    def password_reset(self, request):
        if not request.data or "email" not in request.data:
            return Response({'success': False})
        body = request.data
        resp = requests.post('http://localhost:8000/auth/password_reset/', data={
            'email': body['email'],
        })
        body_unicode = resp.content.decode('utf-8')
        body = json.loads(body_unicode)
        if resp:
            return Response({'success': True, 'message':'Email sent'})
        return Response({'success': False, 'message': body})

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            resp = requests.post('http://localhost:8000/auth/api-token-verify/', data={
                'token': request.META['HTTP_AUTHORIZATION'],
            })
            body_unicode = resp.content.decode('utf-8')
            body = json.loads(body_unicode)
            if resp and 'token' in body:
                headers = {"Authorization": 'JWT ' + request.META['HTTP_AUTHORIZATION']}
                url = 'http://localhost:8000/auth/rest-auth/logout/'
                resp = requests.post(url, headers=headers)

        return Response({'success': True})
    
    

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://localhost:8000/accounts/github/login/callback/'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/accounts/google/login/callback/'
    client_class = OAuth2Client


###       MAIL RESET PASSWORD

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from django_rest_passwordreset.signals import reset_password_token_created

#       MAIL RESET PASSWORD WRAPPER (to avoid 401/404 response)

class PasswordResetConfirmView(APIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, password
    Returns the success/fail message.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        if 'token' and 'password' in request.data:
            resp = requests.post('http://localhost:8000/auth/password_reset/confirm/', data={
                "password": request.data.get('password'),
                "token": request.data.get('token')
            })
            content = json.loads(resp.content.decode('utf-8'))
            if resp:
                data = {'success': True, 'message': content}
            else:
                data = {'success': False, 'message': content}
            return Response(data)
        return Response({'success': False})


#      SEND MAIL WITH RESET PW LINK  (from django_rest_passwordreset config)
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    ### send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # 'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
        'reset_password_url': "http://localhost:3000/login?key="+reset_password_token.key
    }

    ### render email text
    # email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Hypertube"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@hyperube.42",
        # to:
        [reset_password_token.user.email]
    )
    # msg.attach_alternative(email_html_message, "text/html")
    msg.send()

