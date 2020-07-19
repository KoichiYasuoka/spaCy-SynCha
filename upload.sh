#! /bin/sh
rm -fr build dist spacy_syncha.egg-info
python3 setup.py sdist
git status
twine upload --repository pypi dist/*
exit 0
