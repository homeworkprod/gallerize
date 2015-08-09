# -*- coding: utf-8 -*-

from setuptools import setup


def read_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='gallerize',
    version='0.3.1',
    description='Create a static HTML/CSS image gallery from a bunch of images.',
    long_description=read_readme(),
    license='MIT',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/cc0e/#gallerize',
)
