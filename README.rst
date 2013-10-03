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

- Python_ 2.7+ or 3.3+
- Jinja_ (tested with 2.7.1)
- ImageMagick_ (tested with 6.6.9-7)


Installation
============

It is recommended to create a virtual environment and run gallerize
inside it.

To install ImageMagick_ and virtualenv_ on Debian/Ubuntu:

.. code:: sh

  $ aptitude install imagemagick python-virtualenv

This should also give you a copy of pip_.

Create a virtual environment called `env` in the application path:

.. code:: sh

  $ virtualenv env

Activate it (note the space after the first dot!):

.. code:: sh

  $ . env/bin/activate

Install the dependencies of this application:

.. code:: sh

  $ pip install -r requirements.txt


Tests
=====


Run with py.test
----------------

Install py.test_ as test runner:

.. code:: sh

  $ pip install pytest

Run tests:

.. code:: sh

  $ py.test test_gallerize.py


Run with tox
------------

To easily run tests in different Python interpreters, use tox_:

.. code:: sh

  $ pip install tox
  $ tox

And to test against a single, specific Python interpreter (version 3.3,
in this case):

.. code:: sh

  $ tox -e py33


.. _Python: http://www.python.org/
.. _ImageMagick: http://www.imagemagick.org/
.. _Jinja: http://jinja.pocoo.org/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/
.. _py.test: http://pytest.org/
.. _tox: http://tox.testrun.org/
