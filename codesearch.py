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

    urls = {'search': flask.url_for('search')}

    return flask.render_template(
        'codesearch.html', urls=json.dumps(urls))


@app.route('/ajax/search')
def search():
    term = flask.request.args.get('q')
    query = Search(indexes=['sourcecode'], config=BaseSearchConfig)
    query = query.match(term)
    query = query.select('id', 'path')
    results = query.ask()
    results = [get_row(result) for result in results['result']['items']]
    return uncached(json.dumps(results), mimetype='application/json')


def get_row(result):
    return {
        'ajax_url': flask.url_for('ajax_display', sphinx_id=result['id']),
        'display_url': flask.url_for('display', sphinx_id=result['id']),
        'path': result['path']
    }


@app.route('/display/<int:sphinx_id>')
def display(sphinx_id):

    sourcecode = get_sphinx_data(sphinx_id)
    return flask.render_template('display.html',
                                 filename=os.path.basename(sourcecode['path']),
                                 path=sourcecode['path'],
                                 code=sourcecode['body'])


@app.route('/ajax/display/<int:sphinx_id>')
def ajax_display(sphinx_id):

    sourcecode = get_sphinx_data(sphinx_id)
    return uncached(json.dumps(sourcecode), mimetype='application/json')


def get_sphinx_data(sphinx_id):
    query = Search(indexes=['sourcecode'], config=BaseSearchConfig)
    query = query.filter(id__eq=sphinx_id)
    results = query.ask()
    if len(results['result']['items']) == 0:
        flask.abort(404)

    filename = results['result']['items'][0]['path']

    if not os.path.isfile(filename):
        return filename, 'File not found. Please resphinx_id.'

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

    url = flask.url_for('display', sphinx_id=sphinx_id)

    return {'body': result, 'path': filename, 'url': url}


if __name__ == '__main__':
    main()
