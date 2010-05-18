
Markdown Preprocessor
======================

The Markdown Preprocessor is a Python script designed to add extended features
on top of the excellent Markdown syntax defined by John Gruber.  These additions
are mainly focused on creating larger technical documents without needing to use
something as heavy and syntactically complex as Docbook.

The biggest feature provided by markdown-pp is the generation of a table of
contents for a document, with each item linked to the appropriate section of the
markup.  The table is inserted into the document wherever the preprocessor finds
`!TOC` at the beginning of a line.  Named `<a>` tags are inserted above each
Markdown header, and the headings are numbered hierarchically based on the
heading tag that Markdown would generate.

Example file.mdpp:

	# Document Title

	!TOC

	## Header 1
	### Header 1.a
	## Header 2

The preprocessor would generate the following Markdown-ready document file.md:

	<a name="documenttitle"/>
	# Document Title

	1\. [Header 1](#header1)
	1.1\. [Header 1.a](#header1a)
	2\. [Header 2](#header2)

	<a name="header1"/>
	## Header 1
	<a name="header1a"/>
	### Header 1.a
	<a name="header2"/>
	## Header 2

