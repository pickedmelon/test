from database import add_with_session, execute_with_session, get_with_session
from database import Rawtext, Snippet, Reference


def create_new_rawtext(uri, html):
    return Rawtext(uri=uri, html=html)


def create_snippet(rawtext_id, text):
    return Snippet(rawtext_id=rawtext_id, snippet_text=text)


def create_reference(text):
    return Reference(reference_text=text)


def get_unprocessed_rawtext_ids():
    return [r[0] for r in execute_with_session("select distinct(rawtext.id) from rawtext left JOIN snippet "
                                               "on rawtext_id = rawtext.id where snippet.id is NULL")]

def get_all_rawtext_ids():
    return [r[0] for r in execute_with_session("select id from rawtext")]


def add_bulk(gen, bulk_size=100):
    items = []
    for item in gen:
        items.append(item)
        if len(items) > bulk_size:
            add_with_session(items)
            items = []
    add_with_session(items)


def get_imported_rawtext():
    return [r[0] for r in execute_with_session("select uri from rawtext")]


def get_rawtext_by_id(id):
    return get_with_session(lambda s: s.query(Rawtext).filter(Rawtext.id == id).all())[0];
