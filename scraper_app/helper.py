# -*- coding: utf-8 -*-
# chcp 65001
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

from scraper_app.models import Article


def clearDB():
    Article.objects.all().delete()


def findTag(tag):
    if tag.has_attr("class") and tag["class"] == ["dt"]:
        return True
    elif tag.name == "h3":
        for child in tag.children:
            if child.name == "a":
                return True


def scrapMotorsport():
    links_url = "https://www.motorsport.com/category/motogp/news/"
    article_url = "https://www.motorsport.com/"
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Avg", "Sep", "Oct", "Now", "Dec"]
    page_with_links = urlopen(links_url)
    page_with_links_parsed = BeautifulSoup(page_with_links, 'html.parser')
    links_and_dates = page_with_links_parsed.find_all(findTag)
    re_year = re.compile(
        "<span class=\"year\">(?P<year>[0-9]{4})</span>")
    re_month = re.compile(
        "<span class=\"month\">(?P<month>[a-zA-z]{3})</span>")
    re_day = re.compile(
        "<span class=\"date\">(?P<day>[0-9]+)</span>")
    current_date = None
    current_month = None
    current_year = None
    for tag in links_and_dates:
        if tag.has_attr("class") and tag["class"] == ["dt"]:
            for child in [str(child) for child in tag.contents]:
                if re_year.match(child):
                    current_year = str(re_year.match(child).group("year"))
                if re_month.match(child):
                    current_month = str(re_month.match(child).group("month"))
                if re_day.match(child):
                    current_date = str(re_day.match(child).group("day"))
        elif tag.name == "h3":
            for child in tag.contents:
                if child.name == "a":
                    racing_class_re = re.compile(
                        "https://www.motorsport.com/(?P<raceClass>f1)/.*")
                    if not racing_class_re.match(article_url + child["href"]):
                        title = child.string
                        href = article_url + child["href"]
                        article_page = urlopen(href)
                        article_page_parsed = BeautifulSoup(
                            article_page,
                            'html.parser')
                        try:
                            preview = article_page_parsed.find_all(
                                "h2", class_="preview")[0].text
                        except IndexError:
                            preview = "No preview!"
                        text = article_page_parsed.select(".content p")
                        for i in range(len(text)):
                            text[i] = "".join(text[i].text)
                        text = "".join(text)
            article = Article(
                article_title=title,
                article_description=preview,
                article_link=href,
                article_text=text,
                article_source="Motorsport.com",
                article_date="-".join([
                    current_year,
                    str(months.index(current_month) + 1),
                    current_date]))
            article.save()


def scrapCrash():
    # Links for news and article page.
    links_url = "http://www.crash.net/motogp/news_archive/1/content"
    article_url = "http://www.crash.net"
    # List for storing dates.
    dates = []
    # Regex for getting date data.
    r_for_date = re.compile(
        "(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<year>[0-9]{4})")
    # Regex for finding scripts in text.
    r_for_scripts = re.compile(
        "\(.*function\(\){.*();")
    # Getting the page with links to articles,
    # and scraping them.
    page_with_links = urlopen(links_url)
    page_with_links_parsed = BeautifulSoup(page_with_links, 'html.parser')
    links_for_articles = page_with_links_parsed.select(
        ".views-field-title .field-content a")
    dates_for_articles = page_with_links_parsed.find_all(
        'span', class_='field-content')
    # Iterate through all dates in page,
    # get year, month and day,
    # and store them in dates list.
    for date in dates_for_articles:
        if r_for_date.match(date.text):
            dates.append(r_for_date.match(date.text))
    # Iterate through all links in page.
    for link_for_article in links_for_articles:
        # Get the article title
        # and check if article is already
        # in db.
        # If it is, stop scraping.
        title = link_for_article.string
        if Article.objects.filter(article_title=title).exists():
            return
        href = article_url + link_for_article["href"]
        article_page = urlopen(href)
        article_page_parsed = BeautifulSoup(article_page, 'html.parser')
        preview = article_page_parsed.select(
            "article .article-information .field .field-items .field-item p")
        text = article_page_parsed.select(
            ".field > .field-items > .field-item p")
        try:
            preview = preview[0].text
        except IndexError:
            preview = text[0].text
        for i in range(len(text)):
            if i == 0:
                text[i] = ''
            else:
                text[i] = str(text[i].text)
        text = "".join(text)
        try:
            article_date = dates[links_for_articles.index(link_for_article)]
            article_month = article_date.group("month")
            article_day = article_date.group("day")
            article_year = article_date.group("year")
            article = Article(
                article_title=title,
                article_description=preview,
                article_link=href,
                article_text=text,
                article_source="Crash.net",
                article_date="-".join([
                    article_year,
                    article_month,
                    article_day]))
            article.save()
        except IndexError:
            pass


def testScrap():
    clearDB()
    print("Database deleted!")
    scrapCrash()
    print("Crash.net scraped!")
    scrapMotorsport()
    print("Motorsport.com scraped!")
