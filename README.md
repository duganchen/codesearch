# Code Search

[![Build Status](https://travis-ci.org/duganchen/codesearch.svg?branch=master)](https://travis-ci.org/duganchen/codesearch)

![screenshot](https://raw.githubusercontent.com/duganchen/codesearch/master/screenshot.png)


Code Search is a [Sphinx](http://sphinxsearch.com)-backed Intranet app for
doing full-text searches of your git repositories. It consists of an indexer
and a search page.

## The Database Backend

The backend consists of both Sphinx and MySQL.

An SQL file, *scripts/create_db.sql*, is provided to initialize MySQL. If you
read through it, you'll see that it connects to mysql @localhost, so run it on
the host the MySQL is deployed on.

## The Indexer

### Initializing the Indexer

In *indexer*, copy *config.sample.yaml* to *config.yaml* and edit it as you see
fit. For example, you might want to change the list of fnmatch patterns that
determine which files will be indexed.

Edit *indexer/site_extensions.py* and override *get_project_name* if you need
custom code to translate an repo path to an actual project name. For example,
some sites might need a database query to go from "/path/to/gitutils.git" to
"GitUtils".

### Initializing the Repository List

Use the included *repos.py* to generate a list of repositories:

	find /absolute_path/to/repositories/ -maxdepth 1 -type d | ./repos.py > repos.yaml

Update repos.yaml whenever your list of repositories changes.

### Indexing the Repositories

*indexer/indexfiles* will convert a directory to Sphinx-ready XML. In
sphinx.conf, set it as the xmlpipe command for an index named *sourcecode*:

	source sourcecode_pipe
	{
		type			= xmlpipe2
		xmlpipe_command = /path/to/indexfiles
	}


	index sourcecode
	{
		source			= sourcecode_pipe
		path			= /path/to/sphinx/indexes/sourcecode
		charset_type	= utf-8
	}

Run Sphinx's indexer whenever an indexed branch (just master in this
implementation), in any repository, is updated:

	indexer --all --rotate

## The Search Page

The rest is a Flask-based web application.

### Customizing the Search Page

In *codesearch/*, copy *config.sample.yaml* to *config.yaml* and change the
mysql_host parameter  if you need to.

Customize *codesearch/site_extensions.py* as needed. By default, search results
link to a built-in display page, but you can override that so that they link to
an external source code browser instead.

See *codesearch/site_extensions_github.py* for an example. It produces search
results that link to the corresponding lines on GitHub.

### Starting the Search Page

Start it up:

	./codesearch.py

When you're satisfied that it works, give it a proper WSGI-based web server
deployment.

## Credits

The favicon is from
[favicon.cc](http://www.favicon.cc/?action=icon&file_id=661515).
