#!/usr/env/bin python

from setuptools import setup


setup(
    name='gallerize',
    version='0.3',
    description='Create a static HTML/CSS image gallery from a bunch of images.',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/cc0e/#gallerize',
    install_requires=[
        'jinja2 >= 2.7.1',
    ],
    test_requires=[
        'pytest >= 2.4.1',
    ],
)
