import connexion
import six

from untitled_project.engine import QueryEngine
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.image import Image  # noqa: E501
from untitled_project.server import util


def image_id_delete(id_):  # noqa: E501
    """Delete the image identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the image to delete.
    :type id_: int

    :rtype: None
    """
    engine = QueryEngine()
    engine.delete_image(id_)
    return None, 204


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
    return Image(id=i.id, url=url, mime=i.mime, caption=i.caption, author=i.author, source=i.source)


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
            data = f.read()
    except FileNotFoundError:
        return Error('404', f'Image file not found'), 404
    except PermissionError:
        return Error('404', f'Permission denied'), 403
    return data, 200, {'Content-Type': i.mime}


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