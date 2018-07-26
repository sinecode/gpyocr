**************************
gpyocr (Google-Python-OCR)
**************************

Python wrapper for `Tesseract OCR <https://github.com/tesseract-ocr/tesseract>`_ and `Google Vision OCR <https://cloud.google.com/vision/>`_ to perform OCR on images and get a confidence value of the results.

Both OCR engines are Google's products. Tesseract is an open source software that needs some tweaks to get good results, especially if performed on images with poorly defined text. Google Vision OCR engine is a commercial product with much better performance, allowing you to skip the pre-processing jobs on the images.

Only Python 3 is supported.

Usage
#####

The **gpyocr** module have two main functions:

- `tesseract_ocr(image, lang='', psm=None, config=''):` it returns a tuple `(<text recognized>, <confidence>)` obtained with Tesseract. The parameters are the same of the `command-line Tesseract tool <https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage>`_ except for the output file.
- `google_vision_ocr(image, langs=None):` it returns a tuple `(<text recognized>, <confidence>)` obtained with Google Vision API. The `langs` parameter is a list of languages to look for during the OCR process. More information about the supported languages are described on `this page <https://cloud.google.com/vision/docs/languages>`_


The parameter `image` could be:

* a path to the image file
* a numpy object (OpenCV)
* an Image object (Pillow/PIL)


It is possible to get some informations about the Tesseract and Google Vision version found in the system with `get_tesseract_version()` and `get_google_vision_version()` respectively.

The installation of the package also provides a command-line tool, please run
::

    $ gpyocr --help

for more information.


Examples
########

This Python script read the text in the image `tests/resources/european-test.png` on this repository.

.. code-block:: python

    import cv2
    from PIL import Image
    import gpyocr

    # print ('The (quick)...', 87.14)
    print(gpyocr.tesseract_ocr('tests/resources/european-test.png'))

    # print ('The (quick) etc...', 98.00)
    print(gpyocr.google_vision_ocr('tests/resources/european-test.png'))

    # support for OpenCV library
    print(gpyocr.tesseract_ocr(cv2.imread('tests/resources/european-test.png'))

    # support for Pillow library
    print(gpyocr.tesseract_ocr(Image.open('tests/resources/european-test.png'))

    # support for tesseract parameters
    print(gpyocr.tesseract_ocr('tests/resources/european-test.png'), lang='ita', psm=7,
                               config='tessedit_char_whitelist=abc')

    # detect Italian and English words with Google Vision
    print(gpyocr.google_vision_ocr('tests/resources/european-test.png'), langs=['en, 'it'])

Please see the unit tests for more examples.


Installation
############

gpyocr is a pip package.
To install it in your Python environment run:
::

    $ pip install gpyocr

If you want to run Tesseract with gpyocr you have to install it in your system. In order to get the confidence value, gpyocr needs Tesseract >= 3.05. You could install Tesseract with the bash script `tesseract_installer.sh` that you find in the repository. If you want Tesseract 3.05 (the stable version) then run:
::

    $ sudo ./tesseract_installer.sh 3.05

If you want to try Tesseract 4.00 (it's still in beta) then run:
::

    $ sudo ./tesseract_installer.sh 4.00

**Note**: this bash script is tested in Ubuntu 18.04 and CentOS 7; if you don't have these systems, there may be problems installing some dependencies

To use Google Cloud Vision API, you have to authenticate with
::

    $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json

Please refer to `their documentation <https://cloud.google.com/vision/docs/libraries>`_ for more information about installing and using Google Vision services.

License
#######

Apache 2.0

How to contribute
#################

This project is developed to be used by a specific application, so it is not very versatile. If you wish to have new features or if you have any kind of problems, please feel free to contact me via e-mail or open an issue here on GitHub.