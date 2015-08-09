# -*- coding: utf-8 -*-

from setuptools import setup


def read_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='gallerize',
    version='0.3.2',
    description='Create a static HTML/CSS image gallery from a bunch of images.',
    long_description=read_readme(),
    license='MIT',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/cc0e/#gallerize',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: File Sharing',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Graphics :: Presentation',
    ],
)
