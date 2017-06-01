import sys
import lucene
from dba import get_imported_rawtext, add_bulk, get_rawtext_by_id, get_all_rawtext_ids
import os
import json
import lxml.html as LH

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField, StoredField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.standard import StandardAnalyzer

if __name__ == "__main__":
  lucene.initVM()
  path = Paths.get('index')
  indexDir = SimpleFSDirectory(path)
  analyzer = StandardAnalyzer()
  writerConfig = IndexWriterConfig(analyzer)
  writer = IndexWriter(indexDir, writerConfig)
 
  print "%d docs in index" % writer.numDocs()
  print "Reading lines from sys.stdin..."
  todo = get_all_rawtext_ids() 
  for n, i in enumerate(todo):
    try:      
      html = get_rawtext_by_id(i).html
      root = LH.fromstring(html)
      text = root.text_content().strip()
    except:
      #print "Failed to parse doc"
      continue
    doc = Document()
    # print text
    doc.add(TextField("text", text, Field.Store.NO))
    doc.add(StoredField("id", i))
    writer.addDocument(doc)
    if n % 1000 == 0: 
        print "Indexed %d files (%d docs in index)" % (n, writer.numDocs())
  print "Closing index of %d docs..." % writer.numDocs()
  writer.close()

