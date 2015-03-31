def is_indexable_line(line):
    '''
    Given a line, returns whether to index that line. Override this if you want
    to, say, not index lines containing passwords.

    The default implmentation just returns True.
    '''

    return True
