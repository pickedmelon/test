import sys
import lucene
 
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.index import DirectoryReader




if __name__ == "__main__":
    lucene.initVM()
    analyzer = StandardAnalyzer()
    path = Paths.get('index')
    indexDir = SimpleFSDirectory(path)
    searcher = IndexSearcher(DirectoryReader.open(indexDir))
 
    query = QueryParser("text", analyzer).parse("certificate")
    MAX = 1000
    hits = searcher.search(query, MAX)
 
    print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
    for hit in hits.scoreDocs:
        print hit.score, hit.doc, hit.toString()
        doc = searcher.doc(hit.doc)
        print doc.get("id")

