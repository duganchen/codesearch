def is_indexable_file(abspath):
    '''
    Given the absolute path to a git blob in a repository, returns whether to
    index that file.

    The default implementation always returns True.
    '''

    return not abspath.endswith('min.js')


def is_indexable_line(line):
    '''
    Given a line, returns whether to index that line. Override this if you want
    to, say, not index lines containing passwords.

    The default implmentation just returns True.
    '''

    return True
