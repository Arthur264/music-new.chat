PACKAGE=app

all: default

default: deps clean

deps:
	pip install -U -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -path '*/__pycache__/*' -delete


