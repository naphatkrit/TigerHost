develop: install-requirements install-test-requirements

install-requirements:
	pip install -e .

install-test-requirements: install-requirements
	pip install "file://`pwd`#egg=tigerhost[tests]"

deploy:
	python setup.py register -r pypi && python setup.py sdist upload -r pypi

deploy-test:
	python setup.py register -r pypitest && python setup.py sdist upload -r pypitest
