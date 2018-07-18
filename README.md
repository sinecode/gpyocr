# pyocr

Python wrapper to [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Google Vision OCR](https://cloud.google.com/vision/) to perform OCR on images and get a confidence value of the result.

This main branch of the repository runs on Python 2.7, if you're looking for Python 3.6 please move to **pyocr3** branch.

## Installation

**pyocr** is a pip package. To install it clone this repository with:

    $ git clone https://github.com/check-emee/pyocr.git

or download the zip file. Then move to the main directory of this repository. To install the library in your Python environment run

    $ pip install -r requirements.txt
    $ pip install .

If you want to run Tesseract with pyocr you have to install it in your system. In order to get the confidence value, **pyocr** needs Tesseract >= 3.05. You could install Tesseract with the bash script **tesseract_installer.sh** in the repository. If you want Tesseract 3.05 (the stable version) then run:

    $ sudo ./tesseract_installer.sh 3.05

If you want to try Tesseract 4.00 (it's still in beta) then run:

    $ sudo ./tesseract_installer.sh 4.00

**Note**: this bash script is tested in Ubuntu 18.04 and CentOS 7; if you don't have these systems, there may be problems installing some dependencies

To use Google Cloud Vision API, you have to authenticate with

    $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-project-credentials.json

Please refer to [their documentation](https://cloud.google.com/vision/docs/libraries) for more informations.

## Usage

The **pyocr** module have two main functions:

- `tesseract_ocr(image, lang='', psm=None, config=''):` it returns the OCR result obtained with Tesseract from the image together with a confidence value.
- `google_vision_ocr(image, lang='', psm=None, config=''):` it returns the OCR result obtained with Google Vision from the image together with a confidence value.


The parameter image could be:
- a path to the image file
- a numpy object (OpenCV)
- an Image object (Pillow/PIL)


It is possible to get some informations about the Tesseract and Google Vision version found in the system with `get_tesseract_version()` and `get_google_vision_version()` respectively.

## Example:

This Python script read the text in the image `tests/resources/european-test.png` on this repository.

    import cv2
    from PIL import Image
    import pyocr

    # print ('The (quick) etc...', 87.14)
    print pyocr.tesseract_ocr('tests/resources/european-test.png')

    # print ('The (quick) etc...', 98.00)
    print pyocr.google_vision_ocr('tests/resources/european-test.png')

    # print ('The (quick) etc...', 87.14)
    print pyocr.tesseract_ocr(cv2.imread('tests/resources/european-test.png'))

    # print ('The (quick) etc...', 87.14)
    print pyocr.tesseract_ocr(Image.open('tests/resources/european-test.png'))

Please see the unit tests for more examples.
