import time
from multiprocessing import Process, Pool

from django.shortcuts import render

from scraper_app.models import Article
from scraper_app.helper import scrapMotorsport, scrapCrash


def home(request):
    #p1 = Process(target=scrapMotorsport)
    #p2 = Process(target=scrapCrash)
    #p1.start()
    #p2.start()
    #p1.join()
    #p2.join()
    scrapMotorsport()
    scrapCrash()
    articles = Article.objects.all().order_by(
        "-article_date",
        "-article_created")
    return render(
        request,
        'base.html',
        {'articles': articles})
