# -*- coding: utf-8 -*-
# chcp 65001
import re
import time
from urllib.request import urlopen
from django.db import IntegrityError
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
    start_time = time.time()
    # Links for news and article page.
    links_url = "https://www.motorsport.com/category/motogp/news/"
    article_url = "https://www.motorsport.com/"
    # List with months as on the webpage.
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Avg", "Sep", "Oct", "Now", "Dec"]
    # Regex for year, month and day.
    re_year = re.compile(
        "<span class=\"year\">(?P<year>[0-9]{4})</span>")
    re_month = re.compile(
        "<span class=\"month\">(?P<month>[a-zA-z]{3})</span>")
    re_day = re.compile(
        "<span class=\"date\">(?P<day>[0-9]+)</span>")
    re_for_motogp = re.compile(
        "https.*.com//motogp/.*")
    # Variables for storing date parsed from the webpage.
    current_date = None
    current_month = None
    current_year = None
    # Variable for storing articles.
    articles = []
    # Get page with links to articles,
    # and parse it.
    page_with_links = urlopen(links_url)
    page_with_links_parsed = BeautifulSoup(
        page_with_links, 'html.parser')
    links_and_dates = page_with_links_parsed.find_all(
        findTag)
    # Go through every tag and check if it store date or href.
    for tag in links_and_dates:
        if tag.has_attr("class") and tag["class"] == ["dt"]:
            # If tag store date data, get data using regex.
            for child in [str(child) for child in tag.contents]:
                if re_year.match(child):
                    current_year = str(
                        re_year.match(child).group("year"))
                if re_month.match(child):
                    current_month = str(
                        re_month.match(child).group("month"))
                if re_day.match(child):
                    current_date = str(
                        re_day.match(child).group("day"))
        elif tag.name == "h3":
            # Check if element is a link to article,
            # and if it is, get the page and parse it.
            for child in tag.contents:
                if child.name == "a":
                    title = child.string
                    if Article.objects.filter(article_title=title).exists():
                        for article in reversed(articles):
                            try:
                                article.save()
                            except IntegrityError:
                                pass
                        return
                    href = article_url + child["href"]
                    # Check if href is for motogp article.
                    if re_for_motogp.match(href):
                        article_page = urlopen(href)
                        article_page_parsed = BeautifulSoup(
                            article_page,
                            "html.parser")
                        try:
                            # Try to find preview
                            preview = article_page_parsed.find_all(
                                "h2", class_="preview")[0].text
                        except IndexError:
                            preview = "No preview available!"
                        # Get elements with text data
                        text = article_page_parsed.select(
                            ".content p")
                        # Variable for storing text.
                        article_text = ""
                        for i in range(len(text)):
                            article_text = article_text + text[i].text
                        article_text = article_text[:-159]
                        # Instantiating object and adding it to the list.
                        try:
                            article = Article(
                                article_title=title,
                                article_description=preview,
                                article_link=href,
                                article_text=article_text,
                                article_source="Motorsport.com",
                                article_date="-".join([
                                    current_year,
                                    str(months.index(current_month) + 1),
                                    current_date]))
                            articles.append(article)
                        except IndexError:
                            pass
    # Iterate articles list and save each article in db.
    for article in reversed(articles):
        try:
            article.save()
        except IntegrityError:
            pass
    print("scrapMotorsport took %s seconds." % (time.time() - start_time))


def scrapMotorsports():
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
                        "https://www.motorsport.com/f1/.*")
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
    # Lists for storing scraped dates and
    # for storing articles before saving to db.
    dates = []
    articles = []
    # Regex for date
    r_for_date = re.compile(
        "(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<year>[0-9]{4})")
    # Get the page with links to articles
    # and parse it.
    page_with_links = urlopen(
        links_url)
    page_with_links_parsed = BeautifulSoup(
        page_with_links,
        'html.parser')
    # Get all links for articles,
    # and dates.
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
            for article in reversed(articles):
                try:
                    article.save()
                except IntegrityError:
                    pass
            return
        else:
            # Get the page with article
            # and parse it.
            href = article_url + link_for_article["href"]
            article_page = urlopen(href)
            article_page_parsed = BeautifulSoup(
                article_page,
                'html.parser')
            # Remove script and style code from text.
            for script in article_page_parsed(["script", "style"]):
                script.decompose()
            # Get article preview and
            # article text from the page.
            preview = article_page_parsed.select(
                "article .article-information .field .field-items .field-item p")
            text = article_page_parsed.select(
                "article .content > .field > .field-items > .field-item p")
            # Variable for storing text.
            article_text = ""
            # Check if <p> element with preview exist,
            # and if it doesnt get the preview from the text.
            try:
                preview = preview[0].text
            except IndexError:
                try:
                    preview = text[0].text
                except IndexError:
                    preview = "No preview available."
            # Iterate through text (<p> elements)
            for i in range(len(text)):
                if i == 0:
                    article_text = article_text + ""
                else:
                    article_text = article_text + str(text[i].text)
            # Instantiating object and adding it to the list.
            try:
                article_date = dates[
                    links_for_articles.index(link_for_article)]
                article_month = article_date.group("month")
                article_day = article_date.group("day")
                article_year = article_date.group("year")
                article = Article(
                    article_title=title,
                    article_description=preview,
                    article_link=href,
                    article_text=article_text,
                    article_source="Crash.net",
                    article_date="-".join([
                        article_year,
                        article_month,
                        article_day]))
                articles.append(article)
            except IndexError:
                pass
    # Iterate articles list and save each article in db.
    for article in reversed(articles):
        try:
            article.save()
        except IntegrityError:
            pass


def testScrap():
    clearDB()
    print("Database deleted!")
    scrapCrash()
    print("Crash.net scraped!")
    scrapMotorsport()
    print("Motorsport.com scraped!")


import multiprocessing as mp


def cube(x):
    return(x**3)

def test_cube(y):
    start_time = time.time()
    results = [cube(x) for x in range(1,y)]
    print(results)
    print("Took %s seconds." % (time.time() - start_time))


def test_cube_ass(y):
    start_time = time.time()
    pool = mp.Pool(processes=4)
    results = [pool.apply(cube, args=(x, )) for x in range(1,y)]
    print(results)
    print("Took %s seconds." % (time.time() - start_time))
