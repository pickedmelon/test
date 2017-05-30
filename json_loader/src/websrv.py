from flask import Flask
from dba import *
app = Flask(__name__)

@app.route("/")
def hello():
    return get_rawtext_by_id(1).html

@app.route('/view/text/<id>')
def route_text(id):
    return get_rawtext_by_id(id).html

@app.route('/view/detail/<id>')
def route_detail(id):
    buffer = ""
    for i in get_rawtext_by_id(id).snippets:
        buffer += "<p>%s</p>" % i.snippet_text
        for j in i.references:
            buffer += "<p>%s</p>" % i.reference_text
    return buffer


if __name__ == "__main__":
    app.run()