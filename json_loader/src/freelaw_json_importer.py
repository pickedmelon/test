from dba import get_imported_rawtext, add_bulk, get_rawtext_by_id, get_unprocessed_rawtext_ids
from dba import create_reference, create_snippet, create_new_rawtext
import os
import json
import lxml.html as LH
import reference_matcher
PATH = '/Users/ymo/rawdata/'


def generate_rawtext():
    imported = set(get_imported_rawtext())
    count = 0
    skip = 0
    for root, subFolder, files in os.walk(PATH):
        for item in files:
            if item.endswith(".json"):
                file_path = str(os.path.join(root, item))
                jfile = json.load(open(file_path))
                uri = jfile["resource_uri"]
                html = jfile["html_with_citations"]
                if uri not in imported:
                    yield create_new_rawtext(uri, html)
                    count += 1
                else:
                    skip += 1
                if (count + skip) % 1000 == 0:
                    print "imported [ %d ] skipped [%d / %d]" % (count, skip, len(imported))

# add_bulk(generate_rawtext())

def generate_rawtext():
    todo = get_unprocessed_rawtext_ids()
    count = 0
    skip = 0
    for i in todo:
        try:
            html = get_rawtext_by_id(i).html
            root = LH.fromstring(html)
            not_found = True
            for tag_type in ['div', 'p']:
                if not_found:
                    for atag in root.xpath(tag_type):
                        para = atag.text_content().strip()
                        refs = reference_matcher.find_reference(para)
                        # print i, refs
                        if len(refs) > 0:
                            not_found = False
                            snippet = create_snippet(i, para)
                            # print len(refs)
                            for r in refs:
                                snippet.references.append(create_reference(r))
                                # print "found [ %d ] %s" % (i, r)
                            yield snippet
            if not_found:
                skip = skip + 1
            else:
                count = count + 1
            if (count + skip) % 1000 == 0:
                print "imported [ %d ] skipped [ %d ]  [ %d / %d ]" % (count, skip, count + skip, len(todo))
        except:
            pass

add_bulk(generate_rawtext(), bulk_size=100)