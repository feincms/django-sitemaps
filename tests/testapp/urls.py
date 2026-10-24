from django.urls import path

from django_sitemaps import robots_txt


urlpatterns = [
    path("robots.txt", robots_txt()),
]
