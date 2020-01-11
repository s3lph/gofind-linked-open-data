import connexion
import six
import os

from untitled_project.types import place, document, image
from untitled_project.engine import QueryEngine
from untitled_project.server.models.array_of_documents import ArrayOfDocuments  # noqa: E501
from untitled_project.server.models.array_of_images import ArrayOfImages  # noqa: E501
from untitled_project.server.models.array_of_places import ArrayOfPlaces  # noqa: E501
from untitled_project.server.models.document import Document  # noqa: E501
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.image import Image  # noqa: E501
from untitled_project.server.models.place import Place  # noqa: E501
from untitled_project.server import util


def document_id_delete(id_):  # noqa: E501
    """Delete the document identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the document to delete.
    :type id_: int

    :rtype: None
    """
    engine = QueryEngine()
    if engine.delete_document(id_):
        return None, 204
    return Error(code='404', message=f'Document {id_} not found'), 404


def document_id_get(id_):  # noqa: E501
    """Fetch the document identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the document to fetch.
    :type id_: int

    :rtype: Document
    """
    engine = QueryEngine()
    d = engine.query_document(id_)
    if not d:
        return Error('404', f'Document {id_} not found'), 404
    return Document(id=d.id, text=d.text, title=d.title, year=d.year, author=d.author)


def document_id_patch(body, id_):  # noqa: E501
    """Update the document identified by the ID in the path.

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id_: ID number of the document to update.
    :type id_: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = Document.from_dict(connexion.request.get_json())  # noqa: E501
    engine = QueryEngine()
    result = engine.patch_document(id_, body)
    if result:
        return None, 204
    return Error('404', f'Document {id_} not found'), 404


def document_put(body):  # noqa: E501
    """Add a new document

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Document
    """
    if connexion.request.is_json:
        body = Document.from_dict(connexion.request.get_json())  # noqa: E501
    engine = QueryEngine()
    result = engine.put_document(body)
    if result:
        return Document(...), 200
    return Error('400', f'Bad Request'), 400


def image_id_delete(id_):  # noqa: E501
    """Delete the image identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the image to delete.
    :type id_: int

    :rtype: None
    """
    engine = QueryEngine()
    if engine.delete_image(id_):
        return None, 204
    return Error(code='404', message=f'Image {id_} not found'), 404


def image_id_get(id_):  # noqa: E501
    """Fetch the image identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the image to fetch.
    :type id_: int

    :rtype: Image
    """
    engine = QueryEngine()
    i = engine.query_image(id_)
    if not i:
        return Error('404', f'Image {id_} not found'), 404
    url = os.path.join(connexion.request.base_url, 'image')
    return Image(id=i.id, url=url, mime=i.mime, caption=i.caption, copy=i.author)


def image_id_patch(body, id_):  # noqa: E501
    """Update the image identified by the ID in the path.

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id_: ID number of the image to update.
    :type id_: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = Image.from_dict(connexion.request.get_json())  # noqa: E501
    engine = QueryEngine()
    result = engine.patch_image(id_, body)
    if result:
        return None, 204
    return Error('404', f'Image {id_} not found'), 404


def image_id_image_get(id_):  # noqa: E501
    """Fetch the image file belonging to the image object identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the image to fetch.
    :type id_: int

    :rtype: bytearray
    """
    engine = QueryEngine()
    i = engine.query_image(id_)
    if not i:
        return Error('404', f'Image {id_} not found'), 404
    try:
        with open(i.file, 'rb') as f:
            data = bytearray(f.read())
    except FileNotFoundError:
        return Error('404', f'Image file not found'), 404
    except PermissionError:
        return Error('404', f'Permission denied'), 403
    except BaseException:
        return Error('500', f'Internal Server Error'), 500
    return data, 200, {'Content-Type': i.mime}


def image_put(body):  # noqa: E501
    """Add a new image

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Image
    """
    if connexion.request.is_json:
        body = Image.from_dict(connexion.request.get_json())  # noqa: E501
    engine = QueryEngine()
    result = engine.put_image(body)
    if result:
        return Image(id=result.id), 200
    return Error('400', f'Bad Request'), 400


def ping_get():  # noqa: E501
    """ping_get

     # noqa: E501


    :rtype: None
    """
    return None, 204


def place_id_delete(id_):  # noqa: E501
    """Delete the place identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to delete.
    :type id_: int

    :rtype: None
    """
    engine = QueryEngine()
    if engine.delete_place(id_):
        return None, 204
    return Error(code='404', message=f'Place {id_} not found'), 404


def place_id_documents_get(id_):  # noqa: E501
    """Find documents related to the place indicated by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to query for.
    :type id_: int

    :rtype: ArrayOfDocuments
    """
    engine = QueryEngine()
    result = engine.query_documents_for_place(place.Place(id=id_, name=None, lat=None, lon=None, wikidata_id=None))
    return [Document(id=doc.id, text=doc.text, title=doc.title, year=doc.year, author=doc.author) for doc in result]


def place_id_get(id_):  # noqa: E501
    """Fetch the place identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to fetch.
    :type id_: int

    :rtype: Place
    """
    engine = QueryEngine()
    p = engine.query_place(id_)
    if not p:
        return Error('404', f'Place {id_} not found'), 404
    return Place(p.id, p.name, p.lat, p.lon)


def place_id_images_get(id_):  # noqa: E501
    """Find images related to the place indicated by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to query for.
    :type id_: int

    :rtype: ArrayOfImages
    """
    engine = QueryEngine()
    result = engine.query_images_for_place(place.Place(id=id_, name=None, lat=None, lon=None, wikidata_id=None))
    return [Image(id=i.id, data=None, mime=i.mime, caption=i.caption, copy=i.copy) for i in result]


def place_id_patch(body, id_):  # noqa: E501
    """Update the place identified by the ID in the path.

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id_: ID number of the place to update.
    :type id_: int

    :rtype: None
    """
    if connexion.request.is_json:
        body = Place.from_dict(connexion.request.get_json())  # noqa: E501
    engine = QueryEngine()
    result = engine.patch_place(id_, body)
    if result:
        return None, 204
    return Error('404', f'Place {id_} not found'), 404


def place_pid_document_did_delete(pid, did, position_in_text):  # noqa: E501
    """Delete a link between a place identified by pid and a document indicated by did.

     # noqa: E501

    :param pid: ID number of the place
    :type pid: int
    :param did: ID number of the document
    :type did: int
    :param position_in_text: Position of the reference to a place in the document text.
    :type position_in_text: int

    :rtype: None
    """
    engine = QueryEngine()
    result = engine.delete_place_document_link(pid, did, position_in_text)
    if result:
        return None, 204
    return Error('400', f'Place {pid} or document {did} not found'), 400


def place_pid_document_did_get(pid, did):  # noqa: E501
    """Get the links between a place identified by pid and a document indicated by did.

     # noqa: E501

    :param pid: ID number of the place
    :type pid: int
    :param did: ID number of the document
    :type did: int

    :rtype: ArrayOfIntegers
    """
    engine = QueryEngine()
    result = engine.get_place_document_links(pid, did)
    return result


def place_pid_document_did_put(pid, did, position_in_text):  # noqa: E501
    """Add a link between a place identified by pid and a document indicated by did.

     # noqa: E501

    :param pid: ID number of the place
    :type pid: int
    :param did: ID number of the document
    :type did: int
    :param position_in_text: Position of the reference to a place in the document text.
    :type position_in_text: int

    :rtype: None
    """
    engine = QueryEngine()
    result = engine.create_place_document_link(pid, did, position_in_text)
    if result:
        return None, 204
    return Error('400', f'Place {pid} or document {did} does not exist'), 400


def place_pid_image_iid_delete(pid, iid):  # noqa: E501
    """Delete a link between a place identified by pid and an image indicated by iid.

     # noqa: E501

    :param pid: ID number of the place
    :type pid: int
    :param iid: ID number of the image
    :type iid: int

    :rtype: None
    """
    engine = QueryEngine()
    result = engine.delete_place_image_link(pid, iid)
    if result:
        return None, 204
    return Error('400', f'Place {pid} or image {iid} not found'), 400


def place_pid_image_iid_get(pid, iid):  # noqa: E501
    """Get the link between a place identified by pid and an image indicated by iid.

     # noqa: E501

    :param pid: ID number of the place
    :type pid: int
    :param iid: ID number of the image
    :type iid: int

    :rtype: None
    """
    engine = QueryEngine()
    result = engine.get_place_image_link(pid, iid)
    if result:
        return None, 204
    return Error('404', f'Place {pid}, image {iid} not found'), 404


def place_pid_image_iid_put(pid, iid):  # noqa: E501
    """Add a link between a place identified by pid and an image indicated by iid.

     # noqa: E501

    :param pid: ID number of the place
    :type pid: int
    :param iid: ID number of the image
    :type iid: int

    :rtype: None
    """
    engine = QueryEngine()
    result = engine.create_place_image_link(pid, iid)
    if result:
        return None, 204
    return Error('400', f'Place {pid} or image {iid} not found'), 400


def place_put(body):  # noqa: E501
    """Add a new place

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Place
    """
    if connexion.request.is_json:
        body = Place.from_dict(connexion.request.get_json())  # noqa: E501
    engine = QueryEngine()
    result = engine.put_place(body)
    if result:
        return Image(id=result.id), 200
    return Error('400', f'Bad Request'), 400


def places_search_location_get(latitude, longitude, radius=None, limit=None):  # noqa: E501
    """places_search_location_get

     # noqa: E501

    :param latitude: Latitudinal part of the geographical location to find places for, WGS-84.
    :type latitude: float
    :param longitude: Longitudinal part of the geographical location to find places for, WGS-84.
    :type longitude: float
    :param radius: Search radius around the geographical location to find places for, kilometers.
    :type radius: float
    :param limit: Upper limit for the number of places to return.  Use 0 for unlimited.
    :type limit: int

    :rtype: ArrayOfPlaces
    """
    engine = QueryEngine()
    location = (latitude, longitude)
    results = engine.query_location(location, radius, limit)
    return [Place(id=p.id, name=p.name, latitude=p.latitude, longitude=p.longitude) for p, dist in results]


def places_search_name_get(name):  # noqa: E501
    """places_search_name_get

     # noqa: E501

    :param name: Name to search for, case-insensitive.
    :type name: str

    :rtype: ArrayOfPlaces
    """
    engine = QueryEngine()
    results = engine.query_name(name)
    return [Place(id=p.id, name=p.name, latitude=p.latitude, longitude=p.longitude) for p in results]
