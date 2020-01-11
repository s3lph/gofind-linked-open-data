import os
import hashlib

from untitled_project.database.facade import DatabaseFacade
from untitled_project.sources.wikidata import WikidataSource
from untitled_project.types.document import Document
from untitled_project.types.image import Image
from untitled_project.types.place import Place
import untitled_project.server.models as models


IMG_DIR = 'images'


class QueryEngine:

    def __init__(self):
        self._wikidata = WikidataSource()
        self._db = DatabaseFacade(database='foo', user='foo', password='bar')

    def query_place(self, id_) -> Place:
        return self._db.fetch_place(id_)

    def query_document(self, id_) -> Document:
        return self._db.fetch_document(id_)

    def query_image(self, id_) -> Image:
        return self._db.fetch_image(id_)

    def get_place_document_links(self, pid, did):
        return self._db.fetch_place_document_links(pid, did)

    def get_place_image_link(self, pid, iid) -> bool:
        return self._db.has_place_image_link(pid, iid)

    def put_place(self, place: models.place.Place) -> models.place.Place:
        p = Place(id=None,
                  name=place.name,
                  lat=place.latitude,
                  lon=place.longitude,
                  wikidata_id=None)
        return models.place.Place(id=self._db.insert_place(p))

    def put_document(self, document: models.document.Document) -> models.document.Document:
        d = Document(id=None,
                     title=document.title,
                     author=document.author,
                     year=document.year,
                     text=document.text,
                     source=None)
        return models.document.Document(id=self._db.insert_document(d))

    def put_image(self, image: models.image.Image) -> models.image.Image:
        outfile = None
        if image.data:
            digest = hashlib.sha256(image.data).hexdigest()
            outdir = os.path.join(IMG_DIR, digest[:2])
            os.makedirs(outdir, exist_ok=True)
            outfile = os.path.join(outdir, digest)
            with open(outfile, 'wb') as f:
                f.write(image.data)
        i = Image(id=None,
                  file=outfile,
                  mime=image.mime,
                  caption=image.caption,
                  author=image.copy,
                  source=None)
        return models.image.Image(id=self._db.insert_image(i))

    def create_place_document_link(self, pid, did, positon_in_text) -> bool:
        return self._db.insert_place_document_link(pid, did, positon_in_text)

    def create_place_image_link(self, pid, iid) -> bool:
        return self._db.insert_place_image_link(pid, iid)

    def patch_place(self, id_: int, place: models.place.Place) -> models.place.Place:
        p = Place(id=id_,
                  name=place.name,
                  lat=place.latitude,
                  lon=place.longitude,
                  wikidata_id=None)
        return models.place.Place(id=self._db.insert_place(p, ['p_lat', 'p_lon', 'p_name']))

    def patch_document(self, id_: int, document: models.document.Document) -> models.document.Document:
        d = Document(id=id_,
                     title=document.title,
                     author=document.author,
                     year=document.year,
                     text=document.text,
                     source=None)
        return models.document.Document(id=self._db.insert_document(d, ['d_title', 'd_author', 'd_year', 'd_text']))

    def patch_image(self, id_: int, image: models.image.Image) -> models.image.Image:
        outfile = None
        if image.data:
            digest = hashlib.sha256(image.data).hexdigest()
            outdir = os.path.join(IMG_DIR, digest[:2])
            os.makedirs(outdir, exist_ok=True)
            outfile = os.path.join(outdir, digest)
            with open(outfile, 'wb') as f:
                f.write(image.data)
        i = Image(id=id_,
                  file=outfile if outfile else None,
                  mime=image.mime,
                  caption=image.caption,
                  author=image.copy,
                  source=None)
        return models.image.Image(id=self._db.insert_image(i))

    def delete_place(self, id_) -> None:
        self._db.delete_place(id_)

    def delete_document(self, id_) -> None:
        self._db.delete_document(id_)

    def delete_image(self, id_) -> None:
        self._db.delete_image(id_)

    def delete_place_document_link(self, pid, did, position_in_text) -> None:
        self._db.delete_place_document_link(pid, did, position_in_text)

    def delete_place_image_link(self, pid, iid) -> None:
        self._db.delete_place_image_link(pid, iid)

    def query_location(self, location, radius=1.0, limit=10):
        places = []
        local_places = self._db.fetch_places_at_location(location, radius, limit)
        for place in local_places:
            places.append(place)
        wikidata_places = self._wikidata.query_places_at_location(location, radius, limit)
        for place in wikidata_places:
            if len([1 for x in places if x[0].wikidata_id == place[0].wikidata_id]) == 0:
                places.append(place)
        return places

    def query_name(self, name):
        places = []
        local_places = self._db.fetch_places_by_name(name)
        for place in local_places:
            places.append(place)
        wikidata_places = self._wikidata.query_places_by_name(name)
        for place in wikidata_places:
            if len([1 for x in places if x[0].wikidata_id == place[0].wikidata_id]) == 0:
                places.append(place)
        return places

    def query_documents_for_place(self, place):
        documents = []
        if place.id:
            local_documents = self._db.fetch_documents_for_place(place)
            for doc in local_documents:
                documents.append(doc)
        if place.wikidata_id:
            wikidata_documents = self._wikidata.query_documents_for_place(place)
            for doc in wikidata_documents:
                documents.append(doc)
        return documents

    def query_images_for_place(self, place):
        images = []
        if place.id:
            local_images = self._db.fetch_images_for_place(place)
            for img in local_images:
                images.append(img)
        if place.wikidata_id:
            wikidata_images = self._wikidata.query_images_for_place(place)
            for img in wikidata_images:
                images.append(img)
        return images


if __name__ == '__main__':
    QueryEngine().query_location((47.5516427, 7.5964441))
