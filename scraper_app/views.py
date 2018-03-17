import time
from multiprocessing import Process, Pool

from django.shortcuts import render

from scraper_app.models import Article
from scraper_app.helper import scrapMotorsport, scrapCrash


def home(request):
    articles = Article.objects.all().order_by(
        "-article_date",
        "-article_created")
    return render(
        request,
        'base.html',
        {'articles': articles})


def get_data(request):
    start_time = time.time()
    #p1 = Process(target=scrapMotorsport)
    #p2 = Process(target=scrapCrash)
    #p1.start()
    #p2.start()
    #p1.join()
    #p2.join()
    articles = Article.objects.all().order_by(
        "-article_date",
        "-article_created")
    print("Took %s seconds." % (time.time() - start_time))
    return render(
        request,
        'data.html',
        {'articles': articles})
