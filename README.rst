=========
gallerize
=========

Create a static HTML/CSS image gallery from a bunch of images.

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.


Features
========

- Integrates ImageMagick_ to resize images and create thumbnails.
- Generates clean, slim, semantically appropriate HTML5 and uses
  CSS 3 for styling.  As a result, the output can easily be themed.
- Provides HTML access keys for keyboard navigation.
- Optimizes images to reduce size and remove metadata.


Requirements
============

- Python_ 3.7+
- Jinja_
- ImageMagick_ (tested with 6.6.9-7)
- jpegoptim_ (tested with 1.4.6)


Installation
============

It is recommended to create a virtual environment and run gallerize
inside it.

To install ImageMagick_, jpegoptim_, and virtualenv_ on Debian/Ubuntu:

.. code:: sh

  $ aptitude install imagemagick jpegoptim python-virtualenv

This should also give you a copy of pip_.

Create a virtual environment called `venv` in the application path:

.. code:: sh

  $ virtualenv venv

Activate it (note the space after the first dot!):

.. code:: sh

  $ . venv/bin/activate

Install the dependencies of this application:

.. code:: sh

  $ pip install -r requirements.txt

Install gallerize itself:

.. code:: sh

  $ pip install -e .


Tests
=====

Install test dependencies:

.. code:: sh

  $ pip install -r requirements-test.txt

Run tests:

.. code:: sh

  $ pytest


Usage
=====

To create a gallery in the directory `output` from a all images in the
directory `images`:

.. code:: sh

  $ gallerize output/ images/*

See the usage help for more information on specifying a gallery title,
image captions, image dimensions, and more:

.. code:: sh

  $ gallerize --help


.. _Python: http://www.python.org/
.. _ImageMagick: http://www.imagemagick.org/
.. _jpegoptim: https://github.com/tjko/jpegoptim
.. _Jinja: http://jinja.pocoo.org/
.. _virtualenv: http://www.virtualenv.org/
.. _pip: http://www.pip-installer.org/
