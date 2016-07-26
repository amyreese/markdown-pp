readme.md: readme.mdpp
	python bin/markdown-pp readme.mdpp -o readme.md

build: readme.md
	python setup.py build

dev:
	python setup.py develop

upload: readme.md
	python setup.py sdist upload

lint:
	flake8 --show-source .

test: lint
	python bin/markdown-pp readme.mdpp -o readme.test -v && diff -u readme.md readme.test
	rm -f readme.test
	cd test/ && python test.py

clean:
	rm -rf build dist README MANIFEST MarkdownPP.egg-info
