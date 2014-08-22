#!/usr/bin/env python

'''
Generates the repos.yaml file used by the indexer.

Sample usage:

find /path/to/repositories/ -maxdepth 1 -type d | ./repos.py > repos.yaml
'''

import git
import os
import re
import yaml
import sys


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
        match = repo_regex.match(abspath)
        if match is None:
            continue

        repo = match.group('project')

        repos.append(repo)

    print yaml.dump(repos, default_flow_style=False)


if __name__ == '__main__':
    main()
