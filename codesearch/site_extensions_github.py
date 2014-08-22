'''
A sample site-extensions file that links to projects in my personal GitHub
account.
'''

import posixpath
import urlparse


User = 'duganchen'


def get_url(result):

    '''
    Given a MySQL result dictionary, returns the URL to the file.
    '''

    path = posixpath.join(User, result['project'], 'blob', 'master',
                          result['path'])
    return urlparse.urlunsplit(['https', 'github.com', path, '', ''])


def get_line(line_number):

    '''
    Given a line number, returns a string that will be appended after the URL
    hash fragment to link directly to that line.
    '''

    return '#L{}'.format(line_number)
