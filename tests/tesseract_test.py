import os
from pkg_resources import resource_filename

import pytest
import cv2
from PIL import Image

import pyocr

empty_path = os.path.abspath(resource_filename('tests.resources', 'empty.png'))
image_path = os.path.abspath(resource_filename('tests.resources',
                                               'european-test.png'))


def test_invalid_image():
    with pytest.raises(Exception):
        pyocr.tesseract_ocr('invalid/path')


def test_invalid_type():
    with pytest.raises(TypeError):
        pyocr.tesseract_ocr(342)


@pytest.mark.parametrize('image', [
    empty_path, cv2.imread(empty_path), Image.open(empty_path)
])
def test_empty_image(image):
    text, conf = pyocr.tesseract_ocr(image)
    assert text == ''
    assert conf == 0


@pytest.mark.parametrize('image', [
    image_path, cv2.imread(image_path), Image.open(image_path)
])
def test_tesseract_ocr(image):
    text, conf = pyocr.tesseract_ocr(image, lang='eng', psm=4)
    assert len(text) >= 10
    assert '\n' in text
    assert 0 <= conf <= 100


@pytest.mark.parametrize('image', [
    image_path, cv2.imread(image_path), Image.open(image_path)
])
def test_tesseract_ocr_whitelist(image):
    text, conf = pyocr.tesseract_ocr(image,
                                     config='tessedit_char_whitelist=abc')
    assert len(text) >= 10
    assert 'd' not in text
    assert 'e' not in text
    assert 'a' in text
    assert 0 <= conf <= 100
