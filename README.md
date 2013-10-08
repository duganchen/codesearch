# Code Search

Code Search is a [Sphinx](http://sphinxsearch.com)-backed Intranet app for
searching your source code repositories. It consists of an indexer and a search page.

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

Other credits are in the comments, as appropriate.
