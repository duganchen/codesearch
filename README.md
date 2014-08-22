# Code Search

Code Search is a [Sphinx](http://sphinxsearch.com)-backed Intranet app for
searching your source code repositories. It consists of an indexer and a search page.

## Database

An SQL file, *scripts/create_db.sql*, is provided to initialize MySQL.

## Indexer

### Initializing The Indexer

In *indexer*, copy *config.sample.yaml* to *config.yaml* and edit it as you see fit.
For example, you might want to change the list of patterns that determine which files
will be indexed.

Edit *indexer/site_extensions.py* and override *get_project_name* if you custom code
to translate an repo path to an actual project name. For example, some sites might need
a database query to go from "/path/to/gitutils.git" to "GitUtils".

### Initializing The Repository List

Create *indexer/repos.yaml*, containing a list of repositories you want indexed.
A file named *repos.py* has been provided to make it easier:

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

	indexer --all

## Search Page

### Initializing

Customize *codesearch/site_extensions.py* as needed. By default, search results
link to a built-in display page, but you can override that so that they link to
an external source code repository instead. See *codesearch/site_extensions_github.py* for an example.

### Starting

The rest is a Flask-based webapp.

Start it up:

	./codesearch.py

When you're satisfied that it works, give it a proper WSGI-based web server
deployment.

## Note

Both the indexer and the search page assume that the Sphinx index is named
*sourcecode*.

## Credits

The favicon is from
[favicon.cc](http://www.favicon.cc/?action=icon&file_id=661515)

Other credits are in the comments.

## Build Status

[![Build Status](https://travis-ci.org/duganchen/codesearch.svg?branch=master)](https://travis-ci.org/duganchen/codesearch)
