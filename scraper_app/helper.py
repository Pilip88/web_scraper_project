from urllib.request import urlopen
from bs4 import BeautifulSoup


def find_link_value(link):
    first = link.index(">")
    last = link.rindex("<")
    try:
        return link[first:last]
    except ValueError:
        return ""


def scrap():
    articlesDict = {}
    links_url = "https://www.motorsport.com/category/motogp/news/"
    article_url = "https://www.motorsport.com/motogp/news"
    page = urlopen(links_url)
    parse_page = BeautifulSoup(page, 'html.parser')
    articles = parse_page.select(".items .item .wrapper h3 a")
    for article in articles:
        articlesDict[article.string] = article["href"]
    return articlesDict


def scrapMotorsport():
    articlesHrefDict = {}
    articleDict = {}
    articles_url = "https://www.motorsport.com/category/motogp/news/"
    article_url = "https://www.motorsport.com/"
    page_with_links = urlopen(articles_url)
    page_with_links_parsed = BeautifulSoup(page_with_links, 'html.parser')
    articles = page_with_links_parsed.select(".items .item .wrapper h3 a")
    for article in articles:
        articleDict[article.string] = article["href"]
    for article_title in articleDict:
        article_href = article_url + articleDict[article_title]
        article_page = urlopen(article_href)
        article_page_parsed = BeautifulSoup(article_page, 'html.parser')
        """print(article_page_parsed.encode("utf-8"))"""
        """article_title = article_page_parsed.select("#content #preview")"""
        article_preview = article_page_parsed.find_all("h2", class_="preview")[0]
        """article_preview = article_page_parsed.find_all("h2", )
        article_preview = article_page_parsed.select("#page_articles_detail #center_box .article_box #article_detail .article .articleWrapper .articleContent .articleTextBox .content .preview")"""
        articlesHrefDict[article_title] = article_preview
    return articlesHrefDict


def scrapCrash():
    articlesHrefDict = {}
    articleDict = {}
    articles_url = "http://www.crash.net/motogp/news_archive/1/content"
    article_url = "http://www.crash.net"
    page_with_links = urlopen(articles_url)
    page_with_links_parsed = BeautifulSoup(page_with_links, 'html.parser')
    articles = page_with_links_parsed.find_all("a", class_="field_content")
