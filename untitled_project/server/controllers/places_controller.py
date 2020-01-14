import connexion
import six

from untitled_project.engine import QueryEngine
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.place import Place  # noqa: E501
from untitled_project.server import util


def place_id_delete(id_):  # noqa: E501
    """Delete the place identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to delete.
    :type id_: int

    :rtype: None
    """
    engine = QueryEngine()
    engine.delete_place(id_)
    return None, 204


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
    return Place(id=p.id, name=p.name, latitude=p.latitude, longitude=p.longitude, wikidata_id=p.wikidata_id)


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
        return Place(id=result.id), 200
    return Error('400', f'Bad Request'), 400
