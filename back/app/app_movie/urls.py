from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls import url


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'comment', CommentViewSet)
router.register(r'list', MovieViewSet)
router.register(r'player', PlayerView)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('comment', CommentViewSet),
    path('list', MovieViewSet),
    path('player', PlayerView),

]