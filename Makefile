.PHONY: install clean remove upload

install:
	python setup.py install

clean:
	@rm -rf build dist *.egg-info/

upload:
	python setup.py sdist upload
