# Code Search

Code Search is a [Sphinx](http://sphinxsearch.com)-backed Intranet app for
searching your source code repositories. It consists of an indexer and a search page.

## Indexer

*tools/indexfiles* will convert a directory to xmlpipe2-ready XML. Edit it as
necessary. Then, in sphinx.conf, set it as your xmlpipe command:

	source sourcecode_pipe
	{
		type			= xmlpipe2
		xmlpipe_command = /home/dugan/Documents/ember/tools/indexfiles /home/dugan/Documents
	}


	index sourcecode
	{
		source			= sourcecode_pipe
		path			= /var/data/sourcecode
		charset_type	= utf-8
	}

Then run Sphinx's indexer:

	indexer -- all

## Search Page

The rest is a Flask-based webapp with the client-side code written in
CoffeeScript.

First build the CoffeeScript:

	cake build

Then start it up:

	./codesearch.py

## Note

Both the indexer and the search page assume that the Sphinx index is named
*sourcecode*.

## Credits

The favicon is from
[favicon.cc](http://www.favicon.cc/?action=icon&file_id=661515)

Other credits are in the comments.
