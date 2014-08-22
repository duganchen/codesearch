# Code Search

[![Build Status](https://travis-ci.org/duganchen/codesearch.svg?branch=master)](https://travis-ci.org/duganchen/codesearch)

![screenshot](https://raw.githubusercontent.com/duganchen/codesearch/master/screenshot.png)


Code Search is a [Sphinx](http://sphinxsearch.com)-backed Intranet app for
searching your source code repositories. It consists of an indexer and a search
page.

## The Database

An SQL file, *scripts/create_db.sql*, is provided to initialize MySQL.

## The Indexer

### Initializing The Indexer

In *indexer*, copy *config.sample.yaml* to *config.yaml* and edit it as you see
fit. For example, you might want to change the list of fnmatch patterns that
determine which files will be indexed.

Edit *indexer/site_extensions.py* and override *get_project_name* if you need
custom code to translate an repo path to an actual project name. For example,
some sites might need a database query to go from "/path/to/gitutils.git" to
"GitUtils".

### Initializing The Repository List

Create *indexer/repos.yaml*, containing a list of repositories you want
indexed.  A file named *repos.py* has been provided to make it easier:

	find /absolute_path/to/repositories/ -maxdepth 1 -type d | ./repos.py > repos.yaml

Update repos.yaml whenever your list of repositories changes.

### Indexing The Repositories

*indexer/indexfiles* will convert a directory to Sphinx-ready XML. In
sphinx.conf, set it as your xmlpipe command:

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

Then run Sphinx's indexer:

	indexer --all --rotate

## The Search Page

The rest is a Flask-based web application.

### Customizing The Search Page

Customize *codesearch/site_extensions.py* as needed. By default, search results
link to a built-in display page, but you can override that so that they link to
an external source code browser instead.

See *codesearch/site_extensions_github.py* for an example that points results
to GitHub.

### Starting The Search Page

Start it up:

	./codesearch.py

When you're satisfied that it works, give it a proper WSGI-based web server
deployment.

## Credits

The favicon is from
[favicon.cc](http://www.favicon.cc/?action=icon&file_id=661515).
