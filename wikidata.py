#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse

WIKIDATA_API = 'https://query.wikidata.org/sparql?format=json'

WIKIDATA_QUERY='''
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

WIKIPEDIA_API = 'https://de.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=extracts&redirects=1&titles={title}&exintro=1&explaintext=1{cont}'


data = 'query=' + urllib.parse.quote(WIKIDATA_QUERY.format(latitude=47.554822, longitude=7.589263, max_radius=1, limit=10))
request = urllib.request.Request(WIKIDATA_API, data.encode(), method='POST')
response = urllib.request.urlopen(request)
body = json.loads(response.read().decode())['results']['bindings']

postproc = [
    {
        'id': x['a']['value'],
        'title': x['aLabel']['value'],
        'wikipedia_url': x['article']['value'],
        'wikipedia_title': x['article']['value'].split('/')[-1],
        'wikipedia_title_unquot': urllib.parse.unquote(x['article']['value'].split('/')[-1]),
        'image': x['img']['value'] if 'img' in x else None,
        'location': x['location']['value']
    }
    for x in body
]

for lower in range(0,len(postproc),50):
    upper = min(lower + 50, len(postproc))
    titles = '|'.join([x['wikipedia_title'] for x in postproc[lower:upper]])
    cont = ''
    while True:
        data = WIKIPEDIA_API.format(title=titles, cont=cont)
        response = urllib.request.urlopen(data)
        body = json.loads(response.read().decode())
        for normalized in body['query']['normalized']:
            x = [x for x in postproc if x['wikipedia_title_unquot'] == normalized['from']][0]
            x['wikipedia_title'] = normalized['to']
        for page in body['query']['pages']:
            if 'extract' not in page:
                continue
            xs = [x for x in postproc if x['title'] == page['title'] or x['wikipedia_title'] == page['title']]
            if len(xs) == 0:
                continue
            x = xs[0]
            x['abstract'] = page['extract'] if 'extract' in page else None
            x['wikipedia_id'] = page['pageid']
        if 'continue' not in body:
            break
        if body['continue']['excontinue'] == '' or body['continue']['excontinue'] == '||':
            break
        cont = f'&excontinue={body["continue"]["excontinue"]}'

for x in postproc:
    print(x)
    print()
