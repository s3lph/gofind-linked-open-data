from typing import List, Optional

import math

from untitled_project.database.wrapper import DatabaseConnection
from untitled_project.types.place import Place
from untitled_project.types.document import Document
from untitled_project.types.image import Image


class DatabaseFacade:

    def __init__(self, *args, **kwargs):
        self._db = DatabaseConnection(*args, **kwargs)

    def insert_place(self, place: Place, upsert_fields=None):
        upsert_fields = upsert_fields or []
        columns = []
        vcolumns = []
        upsert_columns = []
        values = []

        if place.id is not None:
            columns.append('p_id')
            vcolumns.append('%s')
            values.append(place.id)
        if place.latitude is not None:
            columns.append('p_lat')
            vcolumns.append('%s')
            values.append(place.latitude)
        if place.longitude is not None:
            columns.append('p_lon')
            vcolumns.append('%s')
            values.append(place.longitude)
        if place.name is not None:
            columns.append('p_name')
            vcolumns.append('%s')
            values.append(place.name)
        if place.wikidata_id is not None:
            columns.append('p_wikidata')
            vcolumns.append('%s')
            values.append(place.wikidata_id)
        if len(columns) == 0:
            raise ValueError('Nothing to insert!')

        if place.id is not None and 'p_id' in upsert_fields:
            upsert_columns.append('p_id = %s')
            values.append(place.id)
        if place.latitude is not None and 'p_lat' in upsert_fields:
            upsert_columns.append('p_lat = %s')
            values.append(place.latitude)
        if place.longitude is not None and 'p_lon' in upsert_fields:
            upsert_columns.append('p_lon = %s')
            values.append(place.longitude)
        if place.name is not None and 'p_name' in upsert_fields:
            upsert_columns.append('p_name = %s')
            values.append(place.name)
        if place.wikidata_id is not None and 'p_wikidata' in upsert_fields:
            upsert_columns.append('p_wikidata = %s')
            values.append(place.wikidata_id)

        insert = f'''
        INSERT INTO places ({", ".join(columns)})
        VALUES ({", ".join(vcolumns)})
        '''
        if len(upsert_columns) > 0:
            insert += f' ON DUPLICATE KEY UPDATE {", ".join(upsert_columns)}'

        with self._db.transaction() as c:
            c.execute(insert, tuple(values))
            status = c.rowcount
            if status == 1:
                c.execute('SELECT LAST_INSERT_ID()')
                insert_id, = c.fetchone()
            elif status == 2:
                insert_id = place.id
            else:
                insert_id = -1
        return insert_id

    def update_place(self, place: Place):
        if not place.id:
            raise ValueError('Place ID missing')
        kvpairs = []
        values = []
        if place.latitude:
            kvpairs.append('p_lat = %s')
            values.append(place.latitude)
        if place.longitude:
            kvpairs.append('p_lon = %s')
            values.append(place.longitude)
        if place.name:
            kvpairs.append('p_name = %s')
            values.append(place.name)
        if place.wikidata_id:
            kvpairs.append('p_wikidata = %s')
            values.append(place.wikidata_id)
        if len(kvpairs) == 0:
            raise ValueError('Nothing to update')
        values.append(place.id)
        query = f' UPDATE places SET {", ".join(kvpairs)} WHERE p_id = %s'
        with self._db.transaction() as c:
            c.execute(query, tuple(values))
            if c.rowcount == 0:
                raise ValueError('ID does not exist')
            return place.id

    def insert_document(self, document: Document, upsert_fields=None):
        upsert_fields = upsert_fields or []
        columns = []
        vcolumns = []
        upsert_columns = []
        values = []

        if document.id is not None:
            columns.append('d_id')
            vcolumns.append('%s')
            values.append(document.id)
        if document.title is not None:
            columns.append('d_title')
            vcolumns.append('%s')
            values.append(document.title)
        if document.author is not None:
            columns.append('d_author')
            vcolumns.append('%s')
            values.append(document.author)
        if document.year is not None:
            columns.append('d_year')
            vcolumns.append('%s')
            values.append(document.year)
        if document.text is not None:
            columns.append('d_text')
            vcolumns.append('%s')
            values.append(document.text)
        if document.source is not None:
            columns.append('d_source')
            vcolumns.append('%s')
            values.append(document.source)
        if len(columns) == 0:
            raise ValueError('Nothing to insert!')

        if document.id is not None and 'd_id' in upsert_fields:
            upsert_columns.append('d_id = %s')
            values.append(document.id)
        if document.title is not None and 'd_title' in upsert_fields:
            upsert_columns.append('d_title = %s')
            values.append(document.title)
        if document.author is not None and 'd_author' in upsert_fields:
            upsert_columns.append('d_author = %s')
            values.append(document.author)
        if document.year is not None and 'd_year' in upsert_fields:
            upsert_columns.append('d_year = %s')
            values.append(document.year)
        if document.text is not None and 'd_text' in upsert_fields:
            upsert_columns.append('d_text = %s')
            values.append(document.text)
        if document.source is not None and 'd_source' in upsert_fields:
            upsert_columns.append('d_source = %s')
            values.append(document.source)

        insert = f'''
        INSERT INTO documents ({", ".join(columns)})
        VALUES ({", ".join(vcolumns)})
        '''
        if len(upsert_columns) > 0:
            insert += f' ON DUPLICATE KEY UPDATE {", ".join(upsert_columns)}'

        with self._db.transaction() as c:
            c.execute(insert, tuple(values))
            status = c.rowcount
            if status == 1:
                c.execute('SELECT LAST_INSERT_ID()')
                insert_id, = c.fetchone()
            elif status == 2:
                insert_id = document.id
            else:
                insert_id = -1
        return insert_id

    def update_document(self, document: Document):
        if not document.id:
            raise ValueError('Document ID missing')
        kvpairs = []
        values = []
        if document.title:
            kvpairs.append('d_title = %s')
            values.append(document.title)
        if document.author:
            kvpairs.append('d_author = %s')
            values.append(document.author)
        if document.year:
            kvpairs.append('d_year = %s')
            values.append(document.year)
        if document.text:
            kvpairs.append('d_text = %s')
            values.append(document.text)
        if document.source:
            kvpairs.append('d_source = %s')
            values.append(document.source)
        if len(kvpairs) == 0:
            raise ValueError('Nothing to update')
        values.append(document.id)
        query = f' UPDATE documents SET {", ".join(kvpairs)} WHERE d_id = %s'
        with self._db.transaction() as c:
            c.execute(query, tuple(values))
            if c.rowcount == 0:
                raise ValueError('ID does not exist')
            return document.id

    def insert_image(self, image: Image, upsert_fields=None):
        upsert_fields = upsert_fields or []
        columns = []
        vcolumns = []
        upsert_columns = []
        values = []

        if image.id is not None:
            columns.append('i_id')
            vcolumns.append('%s')
            values.append(image.id)
        if image.file is not None:
            columns.append('i_filepath')
            vcolumns.append('%s')
            values.append(image.file)
        if image.mime is not None:
            columns.append('i_mime')
            vcolumns.append('%s')
            values.append(image.mime)
        if image.caption is not None:
            columns.append('i_caption')
            vcolumns.append('%s')
            values.append(image.caption)
        if image.author is not None:
            columns.append('i_author')
            vcolumns.append('%s')
            values.append(image.author)
        if image.source is not None:
            columns.append('i_source')
            vcolumns.append('%s')
            values.append(image.source)
        if len(columns) == 0:
            raise ValueError('Nothing to insert!')

        if image.id is not None and 'i_id' in upsert_fields:
            upsert_columns.append('i_id = %s')
            values.append(image.id)
        if image.file is not None and 'i_filepath' in upsert_fields:
            upsert_columns.append('i_filepath = %s')
            values.append(image.file)
        if image.mime is not None and 'i_mime' in upsert_fields:
            upsert_columns.append('i_mime = %s')
            values.append(image.mime)
        if image.caption is not None and 'i_caption' in upsert_fields:
            upsert_columns.append('i_caption = %s')
            values.append(image.caption)
        if image.author is not None and 'i_author' in upsert_fields:
            upsert_columns.append('i_author = %s')
            values.append(image.author)
        if image.source is not None and 'i_source' in upsert_fields:
            upsert_columns.append('i_source = %s')
            values.append(image.source)

        insert = f'''
        INSERT INTO images ({", ".join(columns)})
        VALUES ({", ".join(vcolumns)})
        '''
        if len(upsert_columns) > 0:
            insert += f' ON DUPLICATE KEY UPDATE {", ".join(upsert_columns)}'

        with self._db.transaction() as c:
            c.execute(insert, tuple(values))
            status = c.rowcount
            if status == 1:
                c.execute('SELECT LAST_INSERT_ID()')
                insert_id, = c.fetchone()
            elif status == 2:
                insert_id = image.id
            else:
                insert_id = -1
        return insert_id

    def update_image(self, image: Image):
        if not image.id:
            raise ValueError('Image ID missing')
        kvpairs = []
        values = []
        if image.mime:
            kvpairs.append('i_mime = %s')
            values.append(image.mime)
        if image.caption:
            kvpairs.append('i_caption = %s')
            values.append(image.caption)
        if image.author:
            kvpairs.append('i_author = %s')
            values.append(image.author)
        if image.source:
            kvpairs.append('i_source = %s')
            values.append(image.source)
        if len(kvpairs) == 0:
            raise ValueError('Nothing to update')
        values.append(image.id)
        query = f' UPDATE images SET {", ".join(kvpairs)} WHERE i_id = %s'
        with self._db.transaction() as c:
            c.execute(query, tuple(values))
            if c.rowcount == 0:
                raise ValueError('ID does not exist')
            return image.id

    def link_place_document(self, place: Place, document: Document, position_in_text: int):
        if place.id is None or document.id is None:
            raise ValueError()
        insert = '''
        INSERT IGNORE INTO documents_places
        VALUES (%s, %s, %s)
        '''
        with self._db.transaction() as c:
            c.execute(insert, (document.id, place.id, position_in_text))

    def fetch_places_at_location(self, location, radius=1.0, limit=10):
        r2ll = radius / 111.0
        r2 = r2ll * r2ll
        query = '''
        SELECT p_id, p_name, p_wikidata, p_lat, p_lon,
          @dist2 := ((p_lat - %s) * (p_lat - %s) + (p_lon - %s) * (p_lon - %s))
        FROM places
        WHERE @dist2 <= %s
        ORDER BY @dist2 DESC
        LIMIT %s
        '''
        results = []
        with self._db.transaction() as c:
            c.execute(query, (
                location[0], location[0], location[1], location[1],
                r2,
                limit
            ))
            for row in c.fetchall():
                p_id, p_name, p_wikidata, p_lat, p_lon, dist2 = row
                dist = math.sqrt(dist2)
                place = Place(p_id, p_name, p_lat, p_lon, p_wikidata)
                results.append((place, dist))
        return results

    def fetch_places_by_name(self, name, limit=10):
        query = '''
        SELECT p_id, p_name, p_wikidata, p_lat, p_lon
        FROM places
        WHERE p_name LIKE %s
        LIMIT %s
        '''
        results = []
        with self._db.transaction() as c:
            qname = f'%{name.lower()}%'
            c.execute(query, (
                qname,
                limit
            ))
            for row in c.fetchall():
                p_id, p_name, p_wikidata, p_lat, p_lon = row
                place = Place(p_id, p_name, p_lat, p_lon, p_wikidata)
                results.append(place)
        return results

    def fetch_documents_for_place(self, place: Place):
        query = '''
        SELECT d_id, d_title, d_text, d_author, d_year, d_source
        FROM documents
        NATURAL JOIN documents_places
        NATURAL JOIN places
        WHERE p_id = %s
        '''
        results = []
        with self._db.transaction() as c:
            c.execute(query, (place.id,))
            for row in c.fetchall():
                d_id, d_title, d_text, d_author, d_year, d_source = row
                document = Document(d_id, d_title, d_author, d_year, d_text, d_source)
                results.append(document)
        return results

    def fetch_images_for_place(self, place: Place):
        query = '''
        SELECT i_id, i_filepath, i_mime, i_author, i_caption, i_source
        FROM images
        NATURAL JOIN images_places
        NATURAL JOIN places
        WHERE p_id = %s
        '''
        results = []
        with self._db.transaction() as c:
            c.execute(query, (place.id,))
            for row in c.fetchall():
                i_id, i_filepath, i_mime, i_author, i_caption, i_source = row
                image = Image(i_id, i_filepath, i_mime, i_caption, i_author, i_source)
                results.append(image)
        return results

    def fetch_place(self, id_) -> Optional[Place]:
        query = '''
        SELECT p_id, p_name, p_wikidata, p_lat, p_lon
        FROM places
        WHERE p_id = %s
        '''
        with self._db.transaction() as c:
            c.execute(query, (id_,))
            for row in c.fetchall():
                p_id, p_name, p_wikidata, p_lat, p_lon = row
                return Place(id=p_id, name=p_name, latitude=p_lat, longitude=p_lon, wikidata_id=p_wikidata)
        return None

    def fetch_document(self, id_) -> Optional[Document]:
        query = '''
        SELECT d_id, d_title, d_text, d_author, d_year, d_source
        FROM documents
        WHERE d_id = %s
        '''
        with self._db.transaction() as c:
            c.execute(query, (id_,))
            for row in c.fetchall():
                d_id, d_title, d_text, d_author, d_year, d_source = row
                return Document(id=d_id, title=d_title, author=d_author, year=d_year, text=d_text, source=d_source)
        return None

    def fetch_image(self, id_) -> Optional[Image]:
        query = '''
        SELECT i_id, i_filepath, i_mime, i_author, i_caption, i_source
        FROM images
        WHERE i_id = %s
        '''
        with self._db.transaction() as c:
            c.execute(query, (id_,))
            for row in c.fetchall():
                i_id, i_filepath, i_mime, i_author, i_caption, i_source = row
                return Image(id=i_id, file=i_filepath, mime=i_mime, caption=i_caption, author=i_author, source=i_source)
        return None

    def fetch_place_document_links(self, pid, did) -> List[int]:
        query = '''
        SELECT dp_position_in_text
        FROM documents_places
        WHERE d_id = %s
          AND p_id = %s
        '''
        results = []
        with self._db.transaction() as c:
            c.execute(query, (did, pid))
            for row in c.fetchall():
                position, = row
                results.append(position)
        return results

    def has_place_image_link(self, pid, iid) -> bool:
        query = '''
        SELECT 1
        FROM images_places
        WHERE i_id = %s
          AND p_id = %s
        '''
        with self._db.transaction() as c:
            c.execute(query, (iid, pid))
            for _ in c.fetchall():
                return True
        return False

    def insert_place_document_link(self, pid, did, position_in_text) -> bool:
        q1 = 'SELECT 1 FROM places WHERE p_id = %s'
        q2 = 'SELECT 1 FROM documents WHERE d_id = %s'
        q3 = 'INSERT INTO documents_places VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE dp_position_in_text = %s'
        with self._db.transaction() as c:
            c.execute(q1, (pid,))
            if len(c.fetchall()) == 0:
                return False
            c.execute(q2, (did,))
            if len(c.fetchall()) == 0:
                return False
            c.execute(q3, (did, pid, position_in_text, position_in_text))
        return True

    def insert_place_image_link(self, pid, iid) -> bool:
        q1 = 'SELECT 1 FROM places WHERE p_id = %s'
        q2 = 'SELECT 1 FROM images WHERE i_id = %s'
        q3 = 'INSERT INTO images_places VALUES (%s, %s) ON DUPLICATE KEY UPDATE p_id = %s'
        with self._db.transaction() as c:
            c.execute(q1, (pid,))
            if len(c.fetchall()) == 0:
                return False
            c.execute(q2, (iid,))
            if len(c.fetchall()) == 0:
                return False
            c.execute(q3, (iid, pid, pid))
        return True

    def delete_place(self, pid):
        query = 'DELETE FROM places WHERE p_id = %s'
        with self._db.transaction() as c:
            c.execute(query, (pid,))

    def delete_document(self, did):
        query = 'DELETE FROM documents WHERE d_id = %s'
        with self._db.transaction() as c:
            c.execute(query, (did,))

    def delete_image(self, iid):
        query = 'DELETE FROM images WHERE i_id = %s'
        with self._db.transaction() as c:
            c.execute(query, (iid,))

    def delete_place_document_link(self, pid, did, position_in_text):
        query = '''
        DELETE FROM documents_places
        WHERE d_id = %s
          AND p_id = %s
          AND dp_position_in_text = %s
        '''
        with self._db.transaction() as c:
            c.execute(query, (did, pid, position_in_text))

    def delete_place_image_link(self, pid, iid):
        query = '''
        DELETE FROM images_places
        WHERE i_id = %s
          AND p_id = %s
        '''
        with self._db.transaction() as c:
            c.execute(query, (iid, pid))
