from django.urls import path

from scraper_app.views import home

urlpatterns = [
    path("", home, name="home"),
]
