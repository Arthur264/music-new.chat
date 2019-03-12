PACKAGE=app

all: default

default: deps clean test

deps:
	pip install -U -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete
	find . -type f -path '*/.pytest_cache/*' -delete

local_test:
	python -m pytest test/

