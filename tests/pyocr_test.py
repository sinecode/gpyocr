import os
from pkg_resources import resource_filename

import pytest
import cv2
from PIL import Image
from distutils.version import LooseVersion

import pyocr

empty_path = os.path.abspath(resource_filename('tests.resources', 'empty.png'))
image_path = os.path.abspath(resource_filename('tests.resources',
                                               'european-test.png'))


####################################################################
###################### Tesseract OCR ###############################
####################################################################


@pytest.mark.tesseract
def test_tesseract_version():
    tesseract_name, version = pyocr.get_tesseract_version().split(' ')
    assert tesseract_name == 'Tesseract'
    assert LooseVersion(version) >= '3.05'


@pytest.mark.tesseract
def test_invalid_image_tesseract():
    with pytest.raises(Exception):
        pyocr.tesseract_ocr('invalid/path')


@pytest.mark.tesseract
def test_invalid_type_tesseract():
    with pytest.raises(TypeError):
        pyocr.tesseract_ocr(342)


@pytest.mark.tesseract
@pytest.mark.parametrize('image', [
    empty_path, cv2.imread(empty_path), Image.open(empty_path)
])
def test_empty_image_tesseract(image):
    text, conf = pyocr.tesseract_ocr(image)
    assert text == ''
    assert conf == 0


@pytest.mark.tesseract
@pytest.mark.parametrize('image', [
    image_path, cv2.imread(image_path), Image.open(image_path)
])
def test_tesseract_ocr(image):
    text, conf = pyocr.tesseract_ocr(image, lang='eng', psm=4)
    assert len(text) >= 10
    assert text.count('\n') == 11  # text of 12 lines
    assert 0 <= conf <= 100


@pytest.mark.tesseract
@pytest.mark.parametrize('image', [
    image_path, cv2.imread(image_path), Image.open(image_path)
])
def test_tesseract_ocr_whitelist(image):
    text, conf = pyocr.tesseract_ocr(image,
                                     config='tessedit_char_whitelist=abc')
    assert 'd' not in text
    assert 'e' not in text
    assert 'a' in text
    assert 0 <= conf <= 100


####################################################################
###################### Google Vision OCR ###########################
####################################################################


@pytest.mark.googlevision
def test_google_vision_version():
    gv_version = pyocr.get_google_vision_version().split(' ')
    assert gv_version[0] + ' ' + gv_version[1] == 'Google Vision'
    assert LooseVersion(gv_version[2]) >= '0.2'


@pytest.mark.googlevision
def test_invalid_image_google_vision():
    with pytest.raises(Exception):
        pyocr.google_vision_ocr('invalid/path')


@pytest.mark.googlevision
def test_invalid_type_google_vision():
    with pytest.raises(TypeError):
        pyocr.google_vision_ocr(342)


@pytest.mark.googlevision
@pytest.mark.parametrize('image', [
    empty_path, cv2.imread(empty_path), Image.open(empty_path)
])
def test_empty_image_google_vision(image):
    text, conf = pyocr.google_vision_ocr(image)
    assert text == ''
    assert conf == 0


@pytest.mark.googlevision
@pytest.mark.parametrize('image', [
    image_path, cv2.imread(image_path), Image.open(image_path)
])
def test_google_vision_ocr(image, langs=['en']):
    text, conf = pyocr.google_vision_ocr(image)
    assert text.count('\n') == 11  # text of 12 lines
    assert 0 <= conf <= 100
