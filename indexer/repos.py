#!/usr/bin/env python

'''
Generates the repos.yaml file used by the indexer.

Sample usage:

find /path/to/repositories/ -maxdepth 1 -type d | ./repos.py > repos.yaml
'''

import git
import os
import re
from site_extensions import NotProjectError, get_project_name, site_action
import sys
import yaml


def main():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'config.yaml')) as f:
        config = yaml.load(f)

    repo_regex = re.compile(config['project_re'])

    repos = []

    for line in sys.stdin:
        abspath = line.strip()

        if not os.path.isdir(abspath):
            continue

        try:
            git.Repo(abspath)
        except git.errors.InvalidGitRepositoryError:
            # The line is not a git repository. Skip it.
            continue

        try:
            project = get_project_name(abspath, repo_regex)
        except NotProjectError:
            continue

        site_action(abspath, config, repo_regex)

        repos.append({'abspath': abspath, 'project': project})

    print yaml.dump(repos, default_flow_style=False)


if __name__ == '__main__':
    main()
