#!/usr/bin/env python

import flask
import json
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
from sphinxit.core.helpers import BaseSearchConfig
from sphinxit.core.processor import Search


app = flask.Flask(__name__)


def main():
    app.debug = True
    app.run(host='0.0.0.0')


def compose(*args):
    '''
    E.g. composed_function = compose(way_outer, outer, inner, way_inner, ...)
    Composes a chain of functions. Data flows from the function on the right to
    the function on the left, which then returns it. Like in Human Centipede.
    '''
    return reduce(compose2, args)


def compose2(outer, inner):
    '''
    Returns:
        A composed function returning outer(inner(*args, **kwargs))
    '''
    return lambda *args, **kwargs: outer(inner(*args, **kwargs))


def nocache(response):
    # http://stackoverflow.com/a/2068407/240515
    cache_control = 'no-cache, no-store, must-revalidate'
    response.headers['Cache-Control'] = cache_control
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


uncached = compose(nocache, flask.Response)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
def search_page():
    return flask.render_template('codesearch.html')


@app.route('/ajax/search')
def search():
    term = flask.request.args.get('q')
    query = Search(indexes=['sourcecode'], config=BaseSearchConfig)
    query = query.match(term)
    query = query.select('id', 'path')
    results = query.ask()
    get_pair = lambda result: {'id': result['id'], 'path': result['path']}
    pairs = [get_pair(result) for result in results['result']['items']]
    return uncached(json.dumps(pairs), mimetype='application/json')


@app.route('/display/<index>')
def display(index):

    filename, html = get_path_and_content(index)

    return flask.render_template('display.html',
                                 filename=os.path.basename(filename),
                                 path=filename, code=html)


@app.route('/ajax/display/<index>')
def display_ajax(index):

    filename, html = get_path_and_content(index)
    return uncached(html)


def get_path_and_content(index):
    query = Search(indexes=['sourcecode'], config=BaseSearchConfig)
    query = query.filter(id__eq=int(index))
    results = query.ask()
    if len(results['result']['items']) == 0:
        flask.abort(404)

    filename = results['result']['items'][0]['path']

    if not os.path.isfile(filename):
        return filename, 'File not found. Please reindex.'

    code = ''
    with open(filename) as f:
        code = f.read()

    try:
        # This is the line that throws the exception.
        lexer = get_lexer_for_filename(filename)
        formatter = HtmlFormatter(noclasses=True)
        result = highlight(code, lexer, formatter)
    except ClassNotFound:
        # Syntax highlighting not supported.'
        result = '<pre>{}</pre>'.format(code)

    return filename, result


if __name__ == '__main__':
    main()
