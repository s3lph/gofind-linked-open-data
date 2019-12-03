import os
import sys
import hashlib
import pickle

import urllib.request
import lxml.html

from untitled_project.types.document import Document
from untitled_project.types.image import Image
from untitled_project.types.place import Place
from untitled_project.database.facade import DatabaseFacade

BASEURL = 'http://www.basler-bauten.ch'
INDEX = '/'
RAW_OUT_DIR = 'basler_bauten/raw'
IMG_OUT_DIR = 'basler_bauten/images'


def __request(url):
    request = urllib.request.Request(BASEURL + url)
    # Appears to have some kind of User-Agent whitelisting; returns 510 Not Extended when using the default UA
    request.add_header('User-Agent', 'curl/7.67.0')
    response = urllib.request.urlopen(request)
    return response.read(), (response.headers['Content-Type'] or 'application/octet-stream')


def __request_html(url):
    r, _ = __request(url)
    tree = lxml.html.fromstring(r)
    return tree


def __load_obj(fname):
    with open(fname, 'rb') as f:
        name, url, body = pickle.load(f)
    return name, url, body


def cat_list():
    tree = __request_html(INDEX)
    catlist = tree.xpath('//ul[contains(@class, "navbar-nav")]//a')
    categories = []
    for cat in catlist:
        title = cat.xpath('./text()')[0].strip()
        url = cat.xpath('./@href')[0]
        if 'view=category' not in url:
            continue
        categories.append((title, url))
    return categories


def obj_list(cat_url):
    tree = __request_html(cat_url)
    objlist = tree.xpath('//div[@id="t3-content"]//article')
    objects = []
    for obj in objlist:
        title = obj.xpath('.//h2[contains(@class, "article-title")]/text()')[0].strip()
        url = obj.xpath('.//section[contains(@class, "article-intro")]//a/@href')[0]
        if 'view=article' not in url:
            continue
        objects.append((title, url))
    return objects


def obj_dump(obj_name, obj_url):
    body, content_type = __request(obj_url)
    digest = hashlib.sha256(body).hexdigest()
    print(f'Dumping {obj_url} to {digest}')
    with open(os.path.join(RAW_OUT_DIR, digest), 'wb') as f:
        pickle.dump((obj_name, obj_url, body), f)


def obj_parse(fname):
    name, url, body = __load_obj(fname)
    tree = lxml.html.fromstring(body)
    try:
        lat = float(tree.xpath('//head/meta[@name="mapLat"]/@content')[0].strip())
        lon = float(tree.xpath('//head/meta[@name="mapLng"]/@content')[0].strip())
    except ValueError:
        lat = None
        lon = None
    except IndexError:
        lat = None
        lon = None
    try:
        title = tree.xpath('//head/title/text()')[0].strip()
    except IndexError:
        title = None

    # Abuse title as place name; may be helpful for fuzzy matching
    return Place(None, title, lat, lon, None)


def obj_parse_doc(fname):
    name, url, body = __load_obj(fname)
    tree = lxml.html.fromstring(body)
    try:
        title = tree.xpath('//head/title/text()')[0].strip()
    except IndexError:
        title = None
    try:
        author = tree.xpath('//head/meta[@name="author"]/@content')[0].strip()
    except IndexError:
        author = None

    text = ' '.join([t.strip() for t in tree.xpath('//section[contains(@class, "article-content")]//p/text()')])
    return Document(None, title, author, None, text, BASEURL + url)


def obj_parse_images(fname):
    name, url, body = __load_obj(fname)
    tree = lxml.html.fromstring(body)
    images = tree.xpath('//section[contains(@class, "article-content")]//a[contains(@class, "highslide")]/..')
    ret = []
    for itree in images:
        src: str = itree.xpath('.//img/@src')[0]
        try:
            caption: str = itree.xpath('.//div[contains(@class, "highslide-caption")]/text()')[0]
        except IndexError:
            caption = None
        try:
            copy: str = \
                itree.xpath('.//div[contains(@class, "highslide-caption")]/div[contains(@style, "#999999")]/text()')[0]
            if copy.startswith('Quelle: '):
                copy = copy[len('Quelle: '):]
        except IndexError:
            copy = None
        # The website's image URLs are broken, no space escaping done
        src = src.replace(' ', '%20')
        img, mime = __request(src)
        digest = hashlib.sha256(img).hexdigest()
        outdir = os.path.join(IMG_OUT_DIR, digest[:2])
        os.makedirs(outdir, exist_ok=True)
        outfile = os.path.join(outdir, digest)
        with open(outfile, 'wb') as f:
            f.write(img)
        ret.append(Image(None, outfile, mime, caption, copy, BASEURL + url))
    return ret


def dump():
    os.makedirs(RAW_OUT_DIR, exist_ok=True)
    os.makedirs(IMG_OUT_DIR, exist_ok=True)
    categories = cat_list()
    places = []
    for cat, cat_url in categories:
        objs = obj_list(cat_url)
        for obj, obj_url in objs:
            obj_dump(obj, obj_url)


def parse():
    db = DatabaseFacade(database='foo', user='foo', password='bar')
    for fname in os.listdir(RAW_OUT_DIR):
        fullname = os.path.join(RAW_OUT_DIR, fname)
        place = obj_parse(fullname)
        if place.lat is None or place.lon is None:
            continue
        document = obj_parse_doc(fullname)
        # images = obj_parse_images(fullname)
        place.id = db.insert_place(place, upsert_fields=['p_title', 'p_lat', 'p_lon'])
        document.id = db.insert_document(document, upsert_fields=['d_title', 'd_author', 'd_text', 'd_source'])
        db.link_place_document(place, document, 0)
        # for image in images:
        #     db.insert_image(image)


if __name__ == '__main__':
    if sys.argv[1] == 'dump':
        dump()
    elif sys.argv[1] == 'parse':
        parse()
    else:
        raise ValueError()
