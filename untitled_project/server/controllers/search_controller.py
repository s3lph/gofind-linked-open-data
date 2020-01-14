import connexion
import six

from untitled_project.engine import QueryEngine
from untitled_project.server.models.place import Place  # noqa: E501
from untitled_project.server.models.array_of_places import ArrayOfPlaces  # noqa: E501
from untitled_project.server import util


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
    return [Place(id=p.id, name=p.name, latitude=p.latitude, longitude=p.longitude, wikidata_id=p.wikidata_id)
            for p, dist in results]


def places_search_name_get(name):  # noqa: E501
    """places_search_name_get

     # noqa: E501

    :param name: Name to search for, case-insensitive.
    :type name: str

    :rtype: ArrayOfPlaces
    """
    engine = QueryEngine()
    results = engine.query_name(name)
    return [Place(id=p.id, name=p.name, latitude=p.latitude, longitude=p.longitude, wikidata_id=p.wikidata_id)
            for p in results]
