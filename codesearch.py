#!/usr/bin/env python

import flask
import json
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search


app = flask.Flask(__name__)


def main():
    app.debug = True
    app.run(host='0.0.0.0')


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
def search_page():
    return flask.render_template('codesearch.html')


@app.route('/search')
def search():
    term = flask.request.args.get('q')
    query = Search(indexes=['sourcecode'], config=BaseSearchConfig)
    query = query.match(term)
    results = query.ask()
    filenames = [result['path'] for result in results['result']['items']]
    return flask.Response(json.dumps(filenames), mimetype='application/json')


@app.route('/display')
def display():
    filename = flask.request.args.get('f').strip()
    lexer = get_lexer_for_filename(filename)
    formatter = HtmlFormatter(noclasses=True)
    code = ''
    with open(filename) as f:
        code = f.read()
    result = highlight(code, lexer, formatter)

    return flask.render_template('display.html',
                                 filename=os.path.basename(filename),
                                 code=result)


if __name__ == '__main__':
    main()
