'''
Customization hooks for site installations.
'''


def get_project_name(abspath, project_regex):
    '''
    Given the absolute path to a repository and the compiled regex to get the
    project name, returns... the actual project name.

    If the project name cannot be found from the absolute path, then a
    NotProjectError is raised.

    The default implementation simply uses the regex to parse the project name
    out of the path.
    '''

    match = project_regex.match(abspath)
    if match is None:
        raise NotProjectError
    return match.group('project')


def site_initial_action(config):
	'''
	Perform any site-specific action that may be needed on initialization. The default is a no-op.
	'''

	assert config

def site_action(abspath, config, project_regex):
	'''
	Perform any other action that may be needed for the site, per project.

	The default action is a no-op.
	'''
	assert abspath
	assert config
	assert project_regex


class NotProjectError(Exception):
    pass
