import connexion
import six

from untitled_project.engine import QueryEngine
from untitled_project.server.models.document import Document  # noqa: E501
from untitled_project.server.models.error import Error  # noqa: E501
from untitled_project.server import util


def document_id_delete(id_):  # noqa: E501
    """Delete the document identified by the ID in the path.

     # noqa: E501

    :param id_: ID number of the document to delete.
    :type id_: int

    :rtype: None
    """
    engine = QueryEngine()
    engine.delete_document(id_)
    return None, 204


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
    return Document(id=d.id, text=d.text, title=d.title, year=d.year, author=d.author, source=d.source)


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
        return Document(id=result.id), 200
    return Error('400', f'Bad Request'), 400
