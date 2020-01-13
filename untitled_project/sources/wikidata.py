import json
import urllib.request
import urllib.parse

from untitled_project.types.document import Document
from untitled_project.types.image import Image
from untitled_project.types.place import Place

WIKIDATA_API = 'https://query.wikidata.org/sparql?format=json'


WIKIDATA_LOCATION_QUERY = '''
SELECT ?a ?aLabel ?location ?dist ?img ?article
WHERE {{
  ?a wdt:P131 wd:Q78 .
  OPTIONAL {{ ?a wdt:P18 ?img . }} .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "de" . }} .
  SERVICE wikibase:around {{
    ?a wdt:P625 ?location.
    bd:serviceParam wikibase:center "Point({longitude},{latitude})"^^geo:wktLiteral .
    bd:serviceParam wikibase:radius "{max_radius}".
    bd:serviceParam wikibase:distance ?dist.
  }} .
  {{
    ?article schema:about ?a .
    ?article schema:isPartOf <https://de.wikipedia.org/> .
  }} .
}}
ORDER BY ?dist
LIMIT {limit}
'''


WIKIDATA_PLACE_BY_NAME_QUERY = '''
SELECT ?a ?label_de ?label_gsw ?altLabel_de ?altLabel_gsw ?location
WHERE {{
  ?a wdt:P131 wd:Q78 .
  ?a wdt:P625 ?location .
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "de" .
    ?a rdfs:label ?label_de .
    ?a skos:altLabel ?altLabel_de .
  }} .
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "gsw" .
    ?a rdfs:label ?label_gsw .
    ?a skos:altLabel ?altLabel_gsw .
  }} .
  FILTER(
    CONTAINS(LCASE(?label_de), "{name}") ||
    CONTAINS(LCASE(?altLabel_de), "{name}") ||
    CONTAINS(LCASE(?label_gsw), "{name}") ||
    CONTAINS(LCASE(?altLabel_gsw), "{name}")
  ).
}}
LIMIT {limit}
'''


WIKIDATA_NAME_QUERY = '''
SELECT ?a ?label_de ?label_gsw ?altLabel_de ?altLabel_gsw ?article_de ?article_gsw
WHERE {{
  ?a wdt:P131 wd:Q78 .
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "de" .
    ?a rdfs:label ?label_de .
    ?a skos:altLabel ?altLabel_de .
  }} .
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "gsw" .
    ?a rdfs:label ?label_gsw .
    ?a skos:altLabel ?altLabel_gsw .
  }} .
  OPTIONAL {{
    ?article_de schema:about ?a .
    ?article_de schema:isPartOf <https://de.wikipedia.org/> .
  }} .
  OPTIONAL {{
    ?article_gsw schema:about ?a .
    ?article_gsw schema:isPartOf <https://als.wikipedia.org/> .
  }} .
  SERVICE wikibase:around {{
    ?a wdt:P625 ?location.
    bd:serviceParam wikibase:center "Point({longitude},{latitude})"^^geo:wktLiteral .
    bd:serviceParam wikibase:radius "{max_radius}".
    bd:serviceParam wikibase:distance ?dist.
  }} .
}}
ORDER BY ?dist
LIMIT {limit}
'''


WIKIDATA_PLACE_QUERY = '''
SELECT ?a ?aLabel ?location ?dist
WHERE {{
  ?a wdt:P131 wd:Q78 .
  OPTIONAL {{ ?a wdt:P18 ?img . }} .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "de" . }} .
  SERVICE wikibase:around {{
    ?a wdt:P625 ?location.
    bd:serviceParam wikibase:center "Point({longitude},{latitude})"^^geo:wktLiteral .
    bd:serviceParam wikibase:radius "{max_radius}".
    bd:serviceParam wikibase:distance ?dist.
  }} .
}}
ORDER BY ?dist
LIMIT {limit}
'''


WIKIDATA_ARTICLE_QUERY = '''
SELECT ?article
WHERE {{
    ?article schema:about wd:{wikidata_id} .
    ?article schema:isPartOf <https://de.wikipedia.org/> .
}}
'''


WIKIDATA_IMAGE_QUERY = '''
SELECT ?img
WHERE {{
  wd:{wikidata_id} wdt:P18 ?img .
}}
'''


WIKIPEDIA_ARTICLE_API = 'https://de.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=extracts&redirects=1&titles={title}&exintro=1&explaintext=1'


class WikidataSource:

    def __query(self, query):
        data = 'query=' + urllib.parse.quote(query)
        request = urllib.request.Request(WIKIDATA_API, data.encode(), method='POST')
        response = urllib.request.urlopen(request)
        results = json.loads(response.read().decode())['results']['bindings']
        return results

    def __query_wikipedia(self, url):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        results = json.loads(response.read().decode())['query']['pages']
        return results

    def __normalize_value(self, value):
        if not isinstance(value.get('value', None), str):
            return None
        if value.get('type', 'literal') == 'uri':
            *_, v = value['value'].split('/')
            return [urllib.parse.unquote(v).replace('_', ' ')]
        return value['value'].split(', ')

    def __sanitize_input(self, name):
        return name.lower().replace('"', '\\"')

    def query_location(self, location, radius=1, limit=10):
        query = WIKIDATA_LOCATION_QUERY.format(latitude=location[0],
                                               longitude=location[1],
                                               max_radius=radius,
                                               limit=limit)

        results = self.__query(query)
        return results

    def query_name(self, location, radius=1.0, limit=10):
        query = WIKIDATA_NAME_QUERY.format(latitude=location[0],
                                           longitude=location[1],
                                           max_radius=radius,
                                           limit=limit)
        results = []
        for result in self.__query(query):
            if 'a' not in result:
                continue
            a = result['a']
            if 'value' not in a:
                continue
            uri = a['value']
            lbls = set([
                # Flatten list
                x for xs in [
                    r for r in [
                        # Iterate all label keys and get their values
                        self.__normalize_value(result.get(i, {}))
                        for i in ['label_de', 'label_gsw', 'altLabel_de', 'altLabel_gsw', 'article_de', 'article_gsw']
                    ]
                    if r is not None
                ]
                for x in xs
            ])
            # Get last component - the Wikidata ID
            *_, wid = uri.split('/')
            results.append((wid, lbls))
        return results

    def query_places_at_location(self, location, radius=1, limit=10):
        query = WIKIDATA_PLACE_QUERY.format(latitude=location[0],
                                            longitude=location[1],
                                            max_radius=radius,
                                            limit=limit)
        results = self.__query(query)
        places = []
        for result in results:
            wikidata_id = result.get('a', {}).get('value', '').split('/')[-1]
            name = result.get('aLabel', {}).get('value', None)
            # Only process results with a sensible label
            if not name or len(name) == 0 or name == wikidata_id:
                continue
            location = result.get('location', {}).get('value', None)
            if not location or not location.startswith('Point(') or not location.endswith(')'):
                continue
            location = location[6:-1].split(' ')
            if len(location) != 2:
                continue
            try:
                lat = float(location[1])
                lon = float(location[0])
            except ValueError:
                continue
            distance = result.get('dist', {}).get('value', None)
            distance = float(distance) if distance else None
            place = Place(None, name, lat, lon, wikidata_id)
            places.append((place, distance))
        return places

    def query_places_by_name(self, name, limit=10):
        query = WIKIDATA_PLACE_BY_NAME_QUERY.format(name=name.lower(),
                                                    limit=limit)
        results = self.__query(query)
        places = []
        for result in results:
            wikidata_id = result.get('a', {}).get('value', '').split('/')[-1]
            name = result.get('aLabel', {}).get('value', None)
            # Only process results with a sensible label
            if not name or len(name) == 0 or name == wikidata_id:
                continue
            location = result.get('location', {}).get('value', None)
            if not location or not location.startswith('Point(') or not location.endswith(')'):
                continue
            location = location[6:-1].split(' ')
            if len(location) != 2:
                continue
            try:
                lat = float(location[1])
                lon = float(location[0])
            except ValueError:
                continue
            place = Place(None, name, lat, lon, wikidata_id)
            places.append(place)
        return places

    def query_documents_for_place(self, place):
        if not place.wikidata_id:
            return []
        query = WIKIDATA_ARTICLE_QUERY.format(wikidata_id=place.wikidata_id)
        results = self.__query(query)
        documents = []
        for result in results:
            url = result.get('article', {}).get('value', None)
            page = url.split('/')[-1]
            wikipedia_url = WIKIPEDIA_ARTICLE_API.format(title=page)
            response = self.__query_wikipedia(wikipedia_url)
            for article in response:
                article_url = f'https://de.wikipedia.org/wiki/{urllib.parse.quote(article["title"])}'
                doc = Document(id=None,
                               title=article['title'],
                               author=None,
                               year=None,
                               text=article['extract'],
                               source=article_url)
                documents.append(doc)
        return documents

    def query_images_for_place(self, place):
        if not place.wikidata_id:
            return []
        query = WIKIDATA_IMAGE_QUERY.format(wikidata_id=place.wikidata_id)
        results = self.__query(query)
        images = []
        for result in results:
            url = result.get('img', {}).get('value', None)
            images.append(url)
        return images


if __name__ == '__main__':
    s = WikidataSource()
    print(s.query_documents_for_place(Place(None, None, None, None, 'Q381834')))
    print(s.query_images_for_place(Place(None, None, None, None, 'Q381834')))

