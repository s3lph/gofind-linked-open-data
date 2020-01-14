#!/usr/bin/env python3

import urllib.request
import lxml.html
import json
import sys

from untitled_project.database.facade import DatabaseFacade
from untitled_project.types.document import Document

BASEURL = 'https://www.stadtgeschichtebasel.ch'
ARTICLE_LIST = '/index/geschichten.html?view=list'


def dump():
    response = urllib.request.urlopen(BASEURL + ARTICLE_LIST)
    tree = lxml.html.fromstring(response.read())
    alist = tree.xpath('//li[contains(@class, "entry")]')

    articles = []
    for a in alist:
        try:
            href = a.xpath('.//a[contains(@class, "link-text")]/@href')[0]
            title = a.xpath('.//p[contains(@class, "article-title")]/text()')[0]
            title = ' '.join([t.strip() for t in title.split('\n')]).replace('  ', ': ')
            histyear = a.xpath('.//p[contains(@class, "article-year")]/text()')[0]
            print(title)
        except IndexError:
            # Skip meta articles, they don't have an a.link-text
            continue
        # Scrape article
        response = urllib.request.urlopen(BASEURL + href)
        tree = lxml.html.fromstring(response.read())
        text = ' '.join(tree.xpath('//div[contains(@class, "texts")]//text()'))
        articles.append({
            'href': href,
            'title': title,
            'hist_year': histyear,
            'text': text,
            'links': []
        })
        with open(title, 'w') as f:
            f.write(text.lower())

    with open('articles.json', 'w') as f:
        f.write(json.dumps(articles))


def annotate():
    with open('articles.json', 'r') as f:
        articles = json.loads(f.read())
    for article in articles:
        with open(article['title'], 'r') as f:
            atext = f.read()
            positions = [i for i in range(len(atext)) if atext[i].isupper()]
            for position in positions:
                print(article['text'][position:position+50])
                name = input()
                if len(name) > 0:
                    article['links'].append({
                        'name': name,
                        'position_in_text': position
                    })
    with open('articles.json', 'w') as f:
        f.write(json.dumps(articles))


def insert():
    db = DatabaseFacade(database='foo', user='foo', password='bar')
    with open('articles.json', 'r') as f:
        articles = json.loads(f.read())
    for article in articles:
        doc = Document(id=None,
                       title=article['title'],
                       author=None,
                       year=None,
                       text=article['text'],
                       source=BASEURL + article['href'])
        doc.id = db.insert_document(doc, upsert_fields=['d_title', 'd_author', 'd_text', 'd_source'])
        for link in article['links']:
            places = db.fetch_places_by_name(link['name'])
            if places and len(places) > 0:
                db.link_place_document(places[0], doc, link['position_in_text'])


if __name__ == '__main__':
    if sys.argv[1] == 'dump':
        dump()
    elif sys.argv[1] == 'annotate':
        annotate()
    elif sys.argv[1] == 'insert':
        insert()
    else:
        raise ValueError()
