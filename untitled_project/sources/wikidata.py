import json
import urllib.request
import urllib.parse


WIKIDATA_API = 'https://query.wikidata.org/sparql?format=json'


WIKIDATA_QUERY = '''
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


class WikidataSource:

    def query(self, location, radius=1, limit=10):
        data = 'query=' + urllib.parse.quote(
            WIKIDATA_QUERY.format(latitude=location[0],
                                  longitude=location[1],
                                  max_radius=radius,
                                  limit=limit))
        request = urllib.request.Request(WIKIDATA_API, data.encode(), method='POST')
        response = urllib.request.urlopen(request)
        results = json.loads(response.read().decode())['results']['bindings']

        for result in results:
            print(result)


if __name__ == '__main__':
    WikidataSource().query((47.5516427, 7.5964441))
