#!/usr/bin/env python3

import urllib.request
import lxml.html

BASEURL = 'https://www.stadtgeschichtebasel.ch'
INDEX = '/index.html'

response = urllib.request.urlopen(BASEURL + INDEX)
tree = lxml.html.fromstring(response.read())
alist = tree.xpath('//div[contains(@class, "articles-list")]//div[contains(@class, "swiper-slide")]')

articles = []
for a in alist:
    try:
        href = a.xpath('./a/@href')[0]
        title = a.xpath('.//p[contains(@class, "article-title")]/text()')[0]
        histyear = a.xpath('.//p[contains(@class, "article-year")]/text()')[0]
    except IndexError:
        # Skip meta articles
        continue
    # Scrape article
    response = urllib.request.urlopen(BASEURL + href)
    tree = lxml.html.fromstring(response.read())
    text = ' '.join(tree.xpath('//div[contains(@class, "texts")]//text()'))
    articles.append((href, title, histyear, text))

print(articles)

