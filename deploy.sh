#!/usr/bin/env bash

# clear out the dist directory
rm dist/*

# build
python setup.py sdist

# upload
twine upload dist/*

# remove the build
rm dist/*
