
Markdown Preprocessor (MarkdownPP)
==================================

The Markdown Preprocessor is a Python module designed to add extended features
on top of the excellent Markdown syntax defined by John Gruber.  These additions
are mainly focused on creating larger technical documents without needing to use
something as heavy and syntactically complex as Docbook.

MarkdownPP uses a set of selectable modules to apply a series of transforms to
the original document, with the end goal of generating a new Markdown document
that contains sections or features that would be laborious to generate or
maintain by hand.

Documents designed to be preprocessed by MarkdownPP should try to follow the
convention of naming files with a .mdpp extension, so that MarkdownPP can
generate a document with the same name, but with the standard .md extension.
As an example, this document in raw format is named "readme.mdpp", and the
generated document from MarkdownPP is named "readme.md" so that GitHub can find
and process that document when viewing the repository.

1\.  [Modules](#modules)  
1.1\.  [Table of Contents](#tableofcontents)  
1.2\.  [Reference](#reference)  
2\.  [Examples](#examples)  
3\.  [Support](#support)  
4\.  [References](#references)  

<a name="modules"></a>
1\. Modules
--------

<a name="tableofcontents"></a>
### 1.1\. Table of Contents

The biggest feature provided by MarkdownPP is the generation of a table of
contents for a document, with each item linked to the appropriate section of the
markup.  The table is inserted into the document wherever the preprocessor finds
`!TOC` at the beginning of a line.  Named `<a>` tags are inserted above each
Markdown header, and the headings are numbered hierarchically based on the
heading tag that Markdown would generate.

<a name="reference"></a>
### 1.2\. Reference

Similarly, MarkdownPP can generate a list of references that follow Markdown's
alternate link syntax, eg `[name]: <url> "Title"`.  A list of links will be
inserted wherever the preprocessor finds a line beginning with `!REF`.  The
generated reference list follows the same alternate linking method to ensure
consistency in your document, but the link need not be referenced anywhere in
the document to be included in the list.

<a name="examples"></a>
2\. Examples
--------

Example file.mdpp:

	# Document Title

	!TOC

	## Header 1
	### Header 1.a
	## Header 2

	!REF

	[github]: http://github.com "GitHub"

The preprocessor would generate the following Markdown-ready document file.md:

	# Document Title

	1\. [Header 1](#header1)
	1.1\. [Header 1.a](#header1a)
	2\. [Header 2](#header2)

	<a name="header1"></a>
	## Header 1
	<a name="header1a"></a>
	### Header 1.a
	<a name="header2"></a>
	## Header 2

	*	[GitHub][github]

	[github]: http://github.com "GitHub"

<a name="support"></a>
3\. Support
-------

If you find any problems with MarkdownPP, or have any feature requests, please
report them to [my bugtracker][1], and I will respond when possible.  Code
cantributions are *always* welcome.

<a name="references"></a>
4\. References
----------

*	[LeetCode.net Bugtracker][1]

[1]: http://leetcode.net/mantis "LeetCode.net Bugtracker"

