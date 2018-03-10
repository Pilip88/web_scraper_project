from django.shortcuts import render
from django.http import HttpResponse

from scraper_app.models import Article
from scraper_app.helper import scrapMotorsport, scrapCrash


"""
def home(request):
    scrapCrash()
    scrapMotorsport()
    articles = Article.objects.all().order_by(
        "-article_date",
        "-article_created")
    return render(
        request,
        'home.html',
        {'articles': articles})
"""


def home(request):
    return render(
        request,
        'home.html')


def get_data(request):
    scrapCrash()
    scrapMotorsport()
    articles = Article.objects.all().order_by(
        "-article_date",
        "-article_created")
    return render(
        request,
        'data.html',
        {'articles': articles})
