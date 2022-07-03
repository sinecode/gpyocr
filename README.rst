**************************
gpyocr (Google-Python-OCR)
**************************

.. image:: https://img.shields.io/pypi/v/gpyocr.svg
    :target: https://pypi.org/project/gpyocr

.. image:: https://img.shields.io/pypi/l/gpyocr.svg
    :target: https://pypi.org/project/gpyocr

.. image:: https://img.shields.io/pypi/pyversions/gpyocr.svg
    :target: https://pypi.org/project/gpyocr/

.. image:: https://codecov.io/gh/ceccoemi/gpyocr/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ceccoemi/gpyocr

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black



Python wrapper for `Tesseract OCR <https://github.com/tesseract-ocr/tesseract>`_ and `Google Vision OCR <https://cloud.google.com/vision/>`_ to perform OCR on images and get a confidence value of the results.

Both OCR engines are Google's products. Tesseract is an open source software that needs some tweaks to get good results, especially if performed on images with poorly defined text. Google Vision OCR engine is a commercial product with much better performance, allowing you to skip the pre-processing jobs on the images.

Usage
#####

The ``gpyocr`` module have two main functions:

- ``tesseract_ocr(image, lang='', psm=None, config='')``: it returns a tuple
  (*text*, *confidence*) obtained with Tesseract. The parameters are the same of
  the `command-line Tesseract tool <https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage>`_
  except for the output file.
- ``google_vision_ocr(image, langs=None)``: it returns a tuple
  (*text*, *confidence*) obtained with Google Vision API. The `langs` parameter
  is a list of languages to look for during the OCR process. More information
  about the supported languages are described on
  `this page <https://cloud.google.com/vision/docs/languages>`_


The parameter ``image`` could be:

* a string containing the path to the image file
* a numpy object (OpenCV)
* an Image object (Pillow/PIL)


It is possible to get some information about the Tesseract and Google Vision
versions found in the system with ``get_tesseract_version()`` and
``get_google_vision_version()`` respectively.

The installation of the package also provides a command-line tool, please run

.. code-block::

    $ gpyocr --help

for more information.


Examples
########

Examples to read the text in the image ``tests/resources/european-test.png``
on this repository.

.. code-block:: python

    >>> import gpyocr

    >>> gpyocr.tesseract_ocr('tests/resources/european-test.png')
    ('The (quick) [brown] {fox} ... ', 87.13636363636364)

    >>> gpyocr.google_vision_ocr('tests/resources/european-test.png')
    ('The (quick) [brown] {fox} ... ', 98.00000190734863)

    >>> import cv2 # support for OpenCV library
    >>> image = cv2.imread('tests/resources/european-test.png')
    >>> gpyocr.tesseract_ocr(image)
    ('The (quick) [brown] {fox} ... ', 87.13636363636364)

    >>> from PIL import Image # support for Pillow library
    >>> image = Image.open('tests/resources/european-test.png')
    >>> gpyocr.tesseract_ocr(image)
    ('The (quick) [brown] {fox} ... ', 87.13636363636364)

    >>> gpyocr.tesseract_ocr(
        'tests/resources/european-test.png'),
        lang='ita',
        psm=7,
        config='tessedit_char_whitelist=abc',
    )
    ('bc aa cb  b c a ... ', 18.5)

    >>> gpyocr.google_vision_ocr(
        'tests/resources/european-test.png', langs=['en', 'it']
    )
    ('The (quick) [brown] {fox} ... ', 87.13636363636364)

Please see the unit tests for more examples.


Installation
############

``gpyocr`` is a pip package available in the Python Package Index.
To install it in your Python environment run:

.. code-block::

    $ pip install gpyocr

If you want to run Tesseract with gpyocr you have to install it in your
system. In order to get the confidence value, gpyocr needs Tesseract >= 3.05.
You could install Tesseract with the bash script `tesseract_installer.sh` that
you find in the repository. If you want Tesseract 3.05 (the suggested version)
then run:

.. code-block::

    $ sudo ./tesseract_installer 3.05

If you want to try Tesseract 4.1.0 then run:

.. code-block::

    $ sudo ./tesseract_installer 4.1.0

**Note**: this bash script is tested in Ubuntu 18.04 and CentOS 7; if you
don't have these systems, there may be problems installing some dependencies.
You could install all the dependencies by your self and then run:

.. code-block::

    $ sudo ./tesseract_installer.sh 3.05 --no-dependencies


To use Google Cloud Vision API, you have to authenticate with

.. code-block::

    $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json

Please refer to
`their documentation <https://cloud.google.com/vision/docs/libraries>`_ for
more information about installing and using Google Cloud Vision services.

License
#######

Apache 2.0

Testing
#######

First, install ``pytest``, ``pytest-cov`` and ``pytest-mock``. You could
install them with ``pip install -r requirements.txt``.

Go to the root directory of this repository.

To run unit tests without using the OCR libraries run:

.. code-block::

    $ pytest

To run unit tests using the OCR libraries run:

.. code-block::

    $ pytest --nomock

To get a coverage report, run

.. code-block::

    $ pytest --cov --cov-report term-missing

To test only the Tesseract functions run:

.. code-block::

    $ pytest -m tesseract

To test only the Google Cloud Vision functions run:

.. code-block::

    $ pytest -m googlevision

How to contribute
#################

This project is developed to be used by a specific application, so it is not
very versatile. If you wish to have new features or if you have any kind of
problems, please feel free to contact me via e-mail or open an issue here on
GitHub.
