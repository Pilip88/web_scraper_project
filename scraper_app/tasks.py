from celery import task
from scraper_app.helper import scrapMotorsport, scrapCrash


@task()
def scrap_sites():
    print("...................Tasks started")
    scrapMotorsport()
    print("...................scrapMotorsport task finished")
    scrapCrash()
    print("...................scrapCrash task finished")
