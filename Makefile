PYTHON=python3
PIP=pip3
SHELL := /bin/bash

.ONESHELL:
prepare:
	rm -rf dist && true
	$(PYTHON) -m venv ./venv
	source venv/bin/activate
	$(PIP) install -r requirements.txt


.ONESHELL:
test: prepare
	TEST_API_KEY=$(key) $(PYTHON) -m unittest discover -s securenative -p '*_test.py'

.ONESHELL:
publish: test
	$(PIP) install --user --upgrade setuptools wheel
	$(PYTHON) setup.py sdist
	$(PIP) install twine
	twine upload dist/* -u $(twine_user) -p $(twine_pass)