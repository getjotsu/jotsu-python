NAME := jotsu

all: flake8 coverage
.PHONY: all

flake8:
	flake8 app tests
.PHONY: flake8

test:
	PYTHONPATH=. pytest -xv tests
.PHONY: test

coverage:
	PYTHONPATH=. pytest --cov=app --cov-config=.coveragerc --cov-report=term-missing --cov-fail-under=100 -x tests/
.PHONY: coverage

generate:
	curl -sO https://api.jotsu.com/openapi.json
	# openapi-generator-cli generate -g python -o jotsu
.PHONY: generate

freeze:
	./venv/bin/pip3 freeze | egrep -v "egg\=app|pkg-resources|git\+ssh" > requirements.txt
.PHONY: freeze
