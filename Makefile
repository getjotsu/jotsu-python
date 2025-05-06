NAME := jotsu

all: flake8
.PHONY: all

flake8:
	flake8 jotsu
.PHONY: flake8

freeze:
	./venv/bin/pip3 freeze | egrep -v "egg\=jotsu|pkg-resources|git\+ssh" > requirements.txt
.PHONY: freeze
