
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

1\.  [Installation and Usage](#installationandusage)  
2\.  [Modules](#modules)  
2.1\.  [Includes](#includes)  
2.2\.  [Table of Contents](#tableofcontents)  
2.3\.  [Reference](#reference)  
2.4\.  [LaTeX Rendering](#latexrendering)  
3\.  [Examples](#examples)  
4\.  [Support](#support)  
5\.  [References](#references)  

<a name="installationandusage"></a>

1\. Installation and Usage
----------------------

Currently, you'll need to download the source code from [GitHub][2] or clone
the repository.  There are two components to the project: a Python module,
`MarkdownPP`, and a Python script that acts as a simple command line interface
to the module, `markdown-pp.py`.

Assuming you have a file named `foo.mdpp`, you can generate the preprocessed
file `foo.md` by running the following command:

    $ path/to/markdown-pp.py foo.mdpp foo.md

Because the current CLI script is very simple, it just automatically selects
all available modules for the preprocessor to use.  I will eventually get to
the point of adding command parameters and switches to select modules.  In the
mean time, if you only want to use a subset of modules, you can either modify
`markdown-pp.py` directly, or duplicate its usage of the core module with your
own list of preferred modules.

<a name="modules"></a>

2\. Modules
--------

<a name="includes"></a>

### 2.1\. Includes

In order to facilitate large documentation projects, MarkdownPP has an Include
module that will replace a line of the form `!INCLUDE "path/to/filename"` with
the contents of that file, recursively including other files as needed.

File `foo.mdpp`:

	Hello

File `bar.mdpp`:

	World!

File `index.mdpp`:

	!INCLUDE "foo.mdpp"
	!INCLUDE "bar.mdpp"

Compiling `index.mdpp` with the Include module will produce the following:

	Hello
	World!

<a name="tableofcontents"></a>

### 2.2\. Table of Contents

The biggest feature provided by MarkdownPP is the generation of a table of
contents for a document, with each item linked to the appropriate section of the
markup.  The table is inserted into the document wherever the preprocessor finds
`!TOC` at the beginning of a line.  Named `<a>` tags are inserted above each
Markdown header, and the headings are numbered hierarchically based on the
heading tag that Markdown would generate.

<a name="reference"></a>

### 2.3\. Reference

Similarly, MarkdownPP can generate a list of references that follow Markdown's
alternate link syntax, eg `[name]: <url> "Title"`.  A list of links will be
inserted wherever the preprocessor finds a line beginning with `!REF`.  The
generated reference list follows the same alternate linking method to ensure
consistency in your document, but the link need not be referenced anywhere in
the document to be included in the list.

<a name="latexrendering"></a>

### 2.4\. LaTeX Rendering

For example,

	$\displaystyle \int x^2 = \frac{x^3}{3} + C$

becomes

![\displaystyle \int x^2 = \frac{x^3}{3} + C](http://quicklatex.com/cache3/ql_fdd0c74719ed21c7bfec724eceb1ceea_l3.png)

<a name="examples"></a>

3\. Examples
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

4\. Support
-------

If you find any problems with MarkdownPP, or have any feature requests, please
report them to [my bugtracker][1], and I will respond when possible.  Code
contributions are *always* welcome, and ideas for new modules, or additions to
existing modules, are also appreciated.

<a name="references"></a>

5\. References
----------

*	[LeetCode.net Bugtracker][1]
*	[Markdown Preprocessor on GitHub][2]

[1]: http://leetcode.net/mantis "LeetCode.net Bugtracker"
[2]: http://github.com/jreese/markdown-pp "Markdown Preprocessor on GitHub"

