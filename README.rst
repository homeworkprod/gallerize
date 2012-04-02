=========
gallerize
=========

Create a static HTML/CSS image gallery from a bunch of images.


:Copyright: 2007-2012 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
:Version: 0.3
:Date: 02-Apr-2012


Features
========

- Integrates ImageMagick_ to resize images and create thumbnails.
- Generates clean, slim, semantically appropriate HTML5 and uses
  CSS 3 for styling.  As a result, the output can easily be themed.
- Provides HTML access keys for keyboard navigation.


Requirements
============

- Python_ 2.7 or greater
- Jinja_ 2.6 or greater
- ImageMagick_ (tested with 6.6.9-7)


Installation
============

It is recommended to create a virtual environment and run gallerize
inside it.

To install ImageMagick_ and virtualenv_ on Debian/Ubuntu::

  $ aptitude install imagemagick python-virtualenv

This should also give you a copy of pip_.

Create a virtual environment called `env` in the application path::

  $ virtualenv env

Activate it (note the space after the first dot!)::

  $ . env/bin/activate

Install the dependencies of this application::

  $ pip install -r requirements.txt


Tests
=====

Install py.test_ as test runner::

  $ pip install pytest

Run tests::

  $ py.test gallerize_test.py


.. _Python: http://www.python.org/
.. _ImageMagick: http://www.imagemagick.org/
.. _Jinja: http://jinja.pocoo.org/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/
.. _py.test: http://pytest.org/
