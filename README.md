# Code Search

Code Search is a [Sphinx](http://sphinxsearch.com)-based code search solution
for your Intranet.

## Indexer

*tools/indexfiles* will convert a directory to xmlpipe2-ready XML. Edit it as
necessary and set it as your xmlpipe command:

	source sourcecode_pipe
	{
		type = xmlpipe2 xmlpipe_command = /path/to/indexfiles /path/to/repositories
	}

## Search Page

The rest is a Flask-based webapp with the client-side code written in
CoffeeScript.

## Note

Both the indexer and the search page assume that the Sphinx index is named
*sourcecode*.

## Credits

The favicon is from
[favicon.cc](http://www.favicon.cc/?action=icon&file_id=661515)

One function is taken from a blog entry, [Stripping control characters in
Python](http://chase-seibert.github.io/blog/2011/05/20/stripping-control-characters-in-python.html).
