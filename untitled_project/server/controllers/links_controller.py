import connexion
import six

from untitled_project.engine import QueryEngine
from untitled_project.server.models.array_of_documents import ArrayOfDocuments  # noqa: E501
from untitled_project.server.models.array_of_images import ArrayOfImages  # noqa: E501
from untitled_project.server.models.array_of_integers import ArrayOfIntegers  # noqa: E501
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server.models.document import Document  # noqa: E501
from untitled_project.server.models.image import Image  # noqa: E501
from untitled_project.server import util


def place_id_documents_get(id_):  # noqa: E501
    """Find documents related to the place indicated by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to query for.
    :type id_: int

    :rtype: ArrayOfDocuments
    """
    engine = QueryEngine()
    place = engine.query_place(id_)
    result = engine.query_documents_for_place(place)
    return [Document(id=doc.id, text=doc.text, title=doc.title, year=doc.year, author=doc.author, source=doc.source)
            for doc in result]


def place_id_images_get(id_):  # noqa: E501
    """Find images related to the place indicated by the ID in the path.

     # noqa: E501

    :param id_: ID number of the place to query for.
    :type id_: int

    :rtype: ArrayOfImages
    """
    engine = QueryEngine()
    place = engine.query_place(id_)
    result = engine.query_images_for_place(place)
    results = []
    for r in result:
        if isinstance(r, str):
            i = Image(url=r)
        else:
            url = connexion.request.base_url.replace(f'/place/{id_}/images', f'/image/{r.id}/image')
            i = Image(id=r.id, url=url, mime=r.mime, caption=r.caption, author=r.author, source=r.source)
        results.append(i)
    return results


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
    engine.delete_place_document_link(pid, did, position_in_text)
    return None, 204


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
    engine.delete_place_image_link(pid, iid)
    return None, 204


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
    return Error('404', f'Link between place {pid} and image {iid} not found'), 404


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
