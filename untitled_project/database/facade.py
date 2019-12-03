
from untitled_project.database.wrapper import DatabaseConnection
from untitled_project.types.place import Place
from untitled_project.types.document import Document


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
        if place.lat is not None:
            columns.append('p_lat')
            vcolumns.append('%s')
            values.append(place.lat)
        if place.lon is not None:
            columns.append('p_lon')
            vcolumns.append('%s')
            values.append(place.lon)
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
        if place.lat is not None and 'p_lat' in upsert_fields:
            upsert_columns.append('p_lat = %s')
            values.append(place.lat)
        if place.lon is not None and 'p_lon' in upsert_fields:
            upsert_columns.append('p_lon = %s')
            values.append(place.lon)
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
            print(insert)
            c.execute(insert, tuple(values))
            c.execute('SELECT p_id FROM places WHERE p_name = %s', (place.name,))
            insert_id, = c.fetchone()
        return insert_id

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
            c.execute('SELECT d_id FROM documents WHERE d_source = %s', (document.source,))
            insert_id, = c.fetchone()
        return insert_id

    def link_place_document(self, place: Place, document: Document, position_in_text: int):
        if place.id is None or document.id is None:
            raise ValueError
        insert = '''
        INSERT IGNORE INTO documents_places
        VALUES (%s, %s, %s)
        '''
        with self._db.transaction() as c:
            c.execute(insert, (document.id, place.id, position_in_text))
