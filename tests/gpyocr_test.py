import os
from pkg_resources import resource_filename
import string
import subprocess
from collections import namedtuple

import pytest
import cv2
from PIL import Image
from distutils.version import LooseVersion

import gpyocr

empty_path = os.path.abspath(resource_filename('tests.resources', 'empty.png'))
image_path = os.path.abspath(resource_filename(
    'tests.resources', 'european-test.png'
))


###############################################################################
############################# Tesseract OCR ###################################
###############################################################################


@pytest.mark.tesseract
def test_tesseract_version():
    tesseract_name, version = gpyocr.get_tesseract_version().split(' ')
    assert tesseract_name == 'Tesseract'
    assert LooseVersion(version) >= '3.05'


@pytest.mark.tesseract
def test_invalid_image_tesseract():
    with pytest.raises(Exception):
        gpyocr.tesseract_ocr('invalid/path')


@pytest.mark.tesseract
def test_invalid_type_tesseract():
    with pytest.raises(TypeError):
        gpyocr.tesseract_ocr(342)


@pytest.mark.tesseract
@pytest.mark.parametrize(
    'image', [empty_path, cv2.imread(empty_path), Image.open(empty_path)]
)
def test_empty_image_tesseract(image):
    text, conf = gpyocr.tesseract_ocr(image)
    assert text == ''
    assert conf == 0


@pytest.mark.tesseract
@pytest.mark.parametrize(
    'image', [image_path, cv2.imread(image_path), Image.open(image_path)]
)
def test_tesseract_ocr(image):
    text, conf = gpyocr.tesseract_ocr(image, lang='eng', psm=4)
    assert len(text) >= 10
    assert text.count('\n') == 11  # text of 12 lines
    assert 0 <= conf <= 100


@pytest.mark.tesseract
@pytest.mark.parametrize(
    'image', [image_path, cv2.imread(image_path), Image.open(image_path)]
)
def test_tesseract_ocr_whitelist(image):
    text, conf = gpyocr.tesseract_ocr(
        image, config='tessedit_char_whitelist=ab'
    )
    for c in string.ascii_letters.replace('a', '').replace('b', ''):
        assert c not in text
    assert 0 <= conf <= 100


@pytest.fixture
def tesseract_error_mock(monkeypatch):
    def mockocr(*args, **kwargs):
        raise subprocess.CalledProcessError(-1, 'tesseract')
    monkeypatch.setattr(gpyocr._gpyocr.subprocess, 'check_output', mockocr)


@pytest.mark.tesseract
def test_tesseract_error(tesseract_error_mock):
    with pytest.raises(RuntimeError):
        gpyocr.get_tesseract_version()
    with pytest.raises(RuntimeError):
        gpyocr.tesseract_ocr(cv2.imread(image_path))


###############################################################################
############################# Google Vision OCR ###############################
###############################################################################


@pytest.mark.googlevision
def test_google_vision_version():
    version = gpyocr.get_google_vision_version().split(' ')
    assert version[:2] == ['Google', 'Vision']
    assert LooseVersion(version[2]) >= '0.33.0'


@pytest.mark.googlevision
def test_invalid_image_google_vision():
    with pytest.raises(Exception):
        gpyocr.google_vision_ocr('invalid/path')


@pytest.mark.googlevision
def test_invalid_type_google_vision():
    with pytest.raises(TypeError):
        gpyocr.google_vision_ocr(342)


@pytest.fixture
def google_vision_empty_image_mock(monkeypatch):

    Response = namedtuple('Response', 'full_text_annotation')
    TextAnnotation = namedtuple('TextAnnotation', 'text pages')

    class ClientMock:
        def annotate_image(self, *args, **kwargs):
            return Response(TextAnnotation(text='', pages=[]))

    monkeypatch.setattr(
        gpyocr._gpyocr.vision, 'ImageAnnotatorClient', ClientMock
    )


@pytest.mark.googlevision
@pytest.mark.parametrize(
    'image', [empty_path, cv2.imread(empty_path), Image.open(empty_path)]
)
def test_empty_image_google_vision(image, google_vision_empty_image_mock):
    text, conf = gpyocr.google_vision_ocr(image)
    assert text == ''
    assert conf == 0


@pytest.fixture
def google_vision_ocr_mock(monkeypatch):

    Response = namedtuple('Response', 'full_text_annotation')
    TextAnnotation = namedtuple('TextAnnotation', 'text pages')
    Page = namedtuple('TextAnnotation', 'blocks')
    Block = namedtuple('Block', 'confidence')

    class ClientMock:
        def annotate_image(self, *args, **kwargs):
            return Response(TextAnnotation(
                text='\n'.join(('hey' for _ in range(12))),
                pages=[Page(blocks=[Block(confidence=0.88)])]
            ))
    monkeypatch.setattr(
        gpyocr._gpyocr.vision, 'ImageAnnotatorClient', ClientMock
    )


@pytest.mark.googlevision
@pytest.mark.parametrize(
    'image', [image_path, cv2.imread(image_path), Image.open(image_path)]
)
def test_google_vision_ocr(image, google_vision_ocr_mock):
    text, conf = gpyocr.google_vision_ocr(image, langs=['en'])
    assert text.count('\n') == 11  # text of 12 lines
    assert 1 <= conf <= 100
