#!/usr/bin/env python

import collections
import flask
import os
import oursql
import posixpath
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound
import re
import urllib
import yaml

app = flask.Flask(__name__)

from site_extensions import get_url, get_line


def main():
    app.debug = True
    app.run(host='0.0.0.0')


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route('/', methods=['GET', 'POST'])
def search_page():

    if flask.request.method == 'POST':
        term = flask.request.form.get('q', '').strip()
        url = flask.url_for('search_page', q=urllib.quote(term))
        return flask.redirect(url)

    term = urllib.unquote_plus(flask.request.args.get('q', ''))

    results = search(term)

    current_dir = os.path.dirname(os.path.abspath(os.path.join(__file__)))
    update_info_file = os.path.join(current_dir, 'update_info.yaml')
    with open(update_info_file) as f:
        update_info = yaml.load(f)

    date = update_info['last_updated'].strftime('%B %d')
    timestring = update_info['last_updated'].strftime('%Y-%m-%d %H:%M')

    return flask.render_template(
        'codesearch.html', results=results, term=term, title="Code Search",
		date=date, timestring=timestring)


def search(term):
    if len(term) == 0:
        return []

    sphinx = oursql.connect(host='0',  port=9306)

    db = oursql.connect(user='codesearch', passwd='codesearch',
                        db='codesearch')

    # The smallest searchable term is 3 characters.
    if len(term) < 3:
        return []

    attribute_regex = re.compile(r'(@\w+)')

    term_content = get_search_content(term, attribute_regex)
    if has_filters(term, attribute_regex):
        search_term = term
    else:
        search_term = '@content {}'.format(term)

    query = "SELECT id FROM sourcecode WHERE MATCH('{}') LIMIT 1000"
    query = query.format(search_term)
    cursor = sphinx.cursor(oursql.DictCursor)

    try:
        cursor.execute(query, plain_query=True)
    except oursql.ProgrammingError:
        return []

    results = cursor.fetchall()

    if not results:
        return []

    ids = ', '.join([str(int(result['id'])) for result in results])
    query = ''.join(['SELECT id, path, project, text FROM ',
                     'documents WHERE id IN ({})'])
    query = query.format(ids)
    cursor = db.cursor(oursql.DictCursor)
    cursor.execute(query)

    results = cursor.fetchall()

    groups = collections.defaultdict(list)

    for result in results:

        result['url'] = get_url(result)

        text = result['text'].decode('utf-8')

        result['lines'] = []
        if len(term_content) > 0:
            lines = get_matching_lines(result['url'], text, term_content)
            result['lines'] = lines

        if len(result['lines']) > 0:
            result['url'] = result['lines'][0]['url']

        groups[result['project']].append(result)
        del result['project']

    for group, matches in groups.iteritems():
        groups[group] = sorted(matches, key=lambda match: match['path'])

    sorted_groups = []
    for project_name in sorted(groups.keys(), key=lambda x: x.lower()):
        group = {'project': project_name, 'matches': groups[project_name]}
        sorted_groups.append(group)

    return sorted_groups


@app.route('/display/<int:sphinx_id>')
def display(sphinx_id):

    db = oursql.connect(user='codesearch', passwd='codesearch',
                        db='codesearch')

    cursor = db.cursor(oursql.DictCursor)
    query = 'SELECT project, path, text FROM documents WHERE id = ?'
    cursor.execute(query, (sphinx_id,))
    sourcecode = cursor.fetchone()
    if sourcecode is None:
        flask.abort(404)

    title = posixpath.join(sourcecode['project'], sourcecode['path'])

    try:
        lexer = get_lexer_for_filename(sourcecode['path'])
    except ClassNotFound:
        # Syntax highlighting not supported.'
        code = u'<pre>{}</pre>'.format(sourcecode['text'])
        return flask.render_template('display.html', title=title, code=code)

    formatter = HtmlFormatter()

    # Highlighting large files can be a slow operation. This is a candidate
    # for caching.
    code = highlight(sourcecode['text'], lexer, formatter)

    return flask.render_template('display.html', title=title,
                                 code=code)


def get_matching_lines(url, text, term):

    lines = []

    line_number = 0
    for line in text.split('\n'):
        line_number += 1
        # We skip very long lines, e.g. in minified js
        stripped = line.strip()
        if len(stripped) < 2000 and len(stripped) > 0 and term in line:

            line_url = '{}#{}'.format(url, get_line(line_number))
            line = {'number': line_number, 'line': line, 'url': line_url}
            lines.append(line)

    return tuple(lines)


def term_is_valid(term):
    # A search term cannot have mismatched quotation marks
    return term.count('"') % 2 == 0


def get_search_content(query, attribute_regex):
    parts = tuple(x.strip() for x in attribute_regex.split(query) if x.strip())

    if '@content' in parts:
        return parts[parts.index('@content') + 1]

    if not attribute_regex.match(parts[0]):
        return parts[0]

    return ''


def has_filters(query, attribute_regex):
    return any(attribute_regex.match(x.strip()) for x in
               attribute_regex.split(query))


if __name__ == '__main__':
    main()
