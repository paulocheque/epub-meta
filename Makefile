VERSION=0.0.2

clean:
	clear
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	env/bin/python setup.py clean --all
	rm -rf *.egg
	rm -rf *.egg-info/
	rm -rf *.log

prepare:
	clear ; python3.5 -m venv env
	# clear ; virtualenv env -p python2.7

deps:
	clear ; env/bin/pip install -r requirements.txt
	clear ; env/bin/pip install -r requirements-dev.txt

shell:
	clear ; env/bin/python

test:
	@printf "\033[34m====================== TESTING ======================\033[0m\n"
	time env/bin/python -m unittest discover --failfast

test_all:
	tox

coverage:
	env/bin/coverage run -m unittest discover --failfast
	env/bin/coverage report
	env/bin/coverage html
	open htmlcov/index.html

push: test
	git push origin master

compile:
	env/bin/python -OO -m compileall .

lib:
	clear ; env/bin/python setup.py clean --all
	clear ; env/bin/python setup.py test
	clear ; env/bin/python setup.py build

register:
	clear ; env/bin/python setup.py clean --all
	clear ; env/bin/python setup.py sdist
	clear ; env/bin/python setup.py register

publish:
    # http://guide.python-distribute.org/quickstart.html
    # python setup.py sdist
    # python setup.py register
    # Create a .pypirc file in ~ dir (cp .pypirc ~)
    # python setup.py sdist upload
    # Manual upload to PypI
    # http://pypi.python.org/pypi/THE-PROJECT
    # Go to 'edit' link
    # Update version and save
    # Go to 'files' link and upload the file
	clear ; env/bin/python setup.py clean sdist upload

tag:
	git tag ${VERSION}
	git push origin ${VERSION}

reset_tag:
	git tag -d ${VERSION}
	git push origin :refs/tags/${VERSION}
