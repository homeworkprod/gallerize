Changelog
=========


Version 0.4
-----------

Released 2021-05-21

- Added support for Python 3.7, 3.8, and 3.9. Removed support for
  versions older than that.

- Added command line option ``--html-only`` to only regenerate HTML
  files. (contributed by Ryan Daniels)

- Added command line option ``--optimize-images`` to optimize and strip
  metadata from images. (contributed by Ryan Daniels)

- Added command line option ``--version`` to show version number.

- Turned single module into package.

- Added type hints.

- Tweaked HTML and CSS.

- Updated Jinja to 3.0.1 (from 2.11.3).


Version 0.3.2
-------------

Released 2015-08-09

- Added support for Python 3.4.

- A few tweaks here and there.


Version 0.3.1
-------------

Released 2013-10-03

- Added support for Python 3 (3.3, actually).

- Handle missing static path.

- Improved documentation.


Version 0.3
-----------

- Added README.

- Added tests.

- Added option to include image captions from text files.

- Switched from XHTML to HTML5.

- Tweaked template markup and styling. Added CSS transitions.


Version 0.2
-----------

Released 2010-04-02

- Switched image processing from Python Imaging Library (PIL) to
  ImageMagick.

- Switched template engine from Genshi to Jinja 2.

- Merged formerly separate script to resize images into the main script.

- Added option to only copy but not resize images.

- Removed jQuery-based animation (because it became annoying).


Version 0.1
-----------

Released 2007-08-11

- Initially released.
