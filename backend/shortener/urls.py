from django.urls import path
from .views import ShortenURLView, ListShortURLsView

urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name='shorten-url'),
    path('list/', ListShortURLsView.as_view(), name='list-shorturls'),
]
