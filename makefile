readme.md: readme.mdpp
	python bin/markdown-pp readme.mdpp -o readme.md

build: readme.md
	python setup.py build

dev:
	python setup.py develop

upload: readme.md
	python setup.py sdist upload

clean:
	rm -rf build dist README MANIFEST MarkdownPP.egg-info
