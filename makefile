PY=python3

.PHONY: build dev upload lint test clean

readme.md: readme.mdpp
	markdown-pp readme.mdpp -o readme.md

build: readme.md
	$(PY) setup.py build

dev:
	$(PY) setup.py develop

upload: readme.md
	$(PY) setup.py sdist upload

lint:
	flake8 --show-source MarkdownPP

test: lint
	markdown-pp readme.mdpp -o readme.test && diff -u readme.md readme.test
	rm -f readme.test
	cd test/ && $(PY) test.py

clean:
	rm -rf build dist README MANIFEST MarkdownPP.egg-info
