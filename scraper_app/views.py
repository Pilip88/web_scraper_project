from django.shortcuts import render

from scraper_app.models import Article
from scraper_app.helper import scrapMotorsport, scrapCrash


def home(request):
    #scrapMotorsport()
    #scrapCrash()
    articles = Article.objects.all().order_by("-article_date")
    return render(
        request,
        'home.html',
        {'articles': articles})
