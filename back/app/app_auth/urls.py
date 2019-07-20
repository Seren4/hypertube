from django.conf.urls import url, include
from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token, verify_jwt_token
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet),
router.register(r'photo', views.PhotoUploadView),
router.register(r'request', views.RequestsView, basename='request')
# The API URLs are now determined automatically by the router.


# namespacing
app_name = 'app_auth'
urlpatterns = [
    path('reset-pw/', views.PasswordResetConfirmView.as_view(), name='reset password'),
    # drf
    # url(r'^api-auth/', include('rest_framework.urls')),

    # # dr-auth
    url(r'^rest-auth/github/$', csrf_exempt(views.GithubLogin.as_view()), name='github_login'),
    url(r'^rest-auth/', include('rest_auth.urls')),

    # dr-auth-registration
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # url(r'^get_jwt/(?P<access_token>\w{0,50})/$', views.GetJWT),

    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    path('', include(router.urls)),
    path('user', views.UserViewSet),
    path('photo', views.PhotoUploadView),
    path('request', views.RequestsView),

]
