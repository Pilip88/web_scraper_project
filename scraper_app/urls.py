from django.urls import path

from scraper_app.views import home, get_data

urlpatterns = [
    path("", home, name="home"),
    path("get_data", get_data, name="get_data")
]
