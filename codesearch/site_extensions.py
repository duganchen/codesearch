'''
Installation-specific hooks.
'''

import flask


def get_url(result):

    '''
    Given a MySQL result dictionary, returns the URL to the file.

    The default implementation returns the URL to Sphinx's display page.
    '''

    return flask.url_for('display', sphinx_id=result['id'])


def get_line(line_number):

    '''
    Given a line number, returns a string that will be appended after the URL
    hash fragment to link directly to that line.
    '''

    return line_number
