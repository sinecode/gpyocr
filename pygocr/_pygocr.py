'''
Module that contains the wrappers for Tesseract and Google Vision
'''


import os
from tempfile import gettempdir
import string
from random import choice
import subprocess
import csv

import cv2
import numpy as np
from PIL import Image
from google.cloud import vision_v1p1beta1 as vision
import google.cloud.vision


__all__ = ('tesseract_ocr', 'google_vision_ocr', 'SUPPORTED_FORMATS',
           'get_tesseract_version', 'get_google_vision_version')


SUPPORTED_FORMATS = ('gif', 'png', 'jpg', 'jpeg', 'tif', 'tiff')


def get_tesseract_version():
    '''Get Tesseract version'''
    return 'Tesseract {}'.format(
        subprocess.check_output(
            ['tesseract', '--version'],
            stderr=subprocess.STDOUT
        ).decode('utf-8').split()[1])


def get_google_vision_version():
    '''Get Google Vision version'''
    return f'Google Vision {google.cloud.vision.__version__}'


def tesseract_ocr(image, lang='', psm=None, config=''):
    '''Execute a Tesseract call

    Return the text recognized with Tesseract OCR and a confidence
    value of the result. It needs Tesseract >= 3.05
    The image parameter could be:
        - a path to the image file
        - a numpy object (OpenCV)
        - an Image object (Pillow/PIL)
    '''
    if isinstance(image, str):  # check if it's a valid image path
        if not image.lower().endswith(SUPPORTED_FORMATS):
            raise Exception(f'{image} is not a valid image')
        else:
            image_path = image
    else:
        image_path = _get_random_temp_file_name(ext='jpg')
        if isinstance(image, np.ndarray):  # save the Numpy image
            cv2.imwrite(image_path, image)
        elif isinstance(image, Image.Image):  # save the PIL image
            if not image.mode.startswith('RGB'):
                image = image.convert('RGB')
            image.save(image_path)
        else:
            raise TypeError('The image could be a string containing the '
                            'path to the file, it could be a numpy '
                            'object or an Image PIL object')

    output_path = _get_random_temp_file_name()

    # build Tesseract command
    tesseract_cmd = ['tesseract', image_path, output_path]
    if lang:
        tesseract_cmd.append(f'-l {lang}')
    if psm:
        tesseract_cmd.append(f'--psm={psm}')
    if config:
        tesseract_cmd.append('-c')
        tesseract_cmd.append(config)
    tesseract_cmd.append('tsv')  # tsv output to get confidence value

    # execute Tesseract
    subprocess.call(tesseract_cmd, stdin=subprocess.PIPE,
                    stderr=subprocess.PIPE)
    output_path += '.tsv'

    # Read the file created by Tesseract containing the OCR results.
    # The tsv file has various columns, we are interested to the column 'conf'
    # and the column 'text'. The cells of 'text' column are concatenated and
    # with the confidence rates the average is calculated
    text = []
    conf = 0
    conf_num = 0
    with open(output_path) as f:
        reader = csv.DictReader(f, delimiter='\t', quotechar='|')
        text_line = []
        for row in reader:
            c = float(row['conf'])
            if c > 0:
                text_line.append(row['text'])
                conf += c
                conf_num += 1
            else:
                text.append(' '.join(c for c in text_line))
                text_line = []
        text.append(' '.join(c for c in text_line))
    if conf_num > 0:
        conf = conf / conf_num

    # remove the two temporary files: image and output file
    if not isinstance(image, str):
        os.remove(image_path)
    os.remove(output_path)

    # return the tuple (text, confidence)
    return '\n'.join(line for line in text).strip(), conf


def google_vision_ocr(image, langs=None):
    '''Execute a Google Visin OCR call

    Return the text recognized with Google VIson OCR and a confidence
    value of the result.
    The image parameter could be:
        - a path to the image file
        - a numpy object (OpenCV)
        - an Image object (Pillow/PIL)
    '''

    if isinstance(image, str):
        if not image.lower().endswith(SUPPORTED_FORMATS):
            raise Exception(f'{image} is not a valid image')
        with open(image, 'rb') as image_file:
            image = image_file.read()
    elif isinstance(image, np.ndarray):
        # Encode the image to base64
        image = cv2.imencode('.jpg', image)[1].tostring()
    elif isinstance(image, Image.Image):
        # Encode the image to base64
        if not image.mode.startswith('RGB'):
            image = image.convert('RGB')
        image = np.array(image)
        image = cv2.imencode('.jpg', image)[1].tostring()
    else:
        raise TypeError('The image could be a string containing the '
                        'path to the file, it could be a numpy '
                        'object or an Image PIL object')

    # Authenticate to Google Cloud Platform
    # You have to execute:
# $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials-key.json
    client = vision.ImageAnnotatorClient()

    # Perform the request to Google Cloud Vision
    if not langs:
        langs = ['en', 'it']
    response = client.document_text_detection(
        vision.types.Image(content=image),
        image_context=vision.types.ImageContext(language_hints=langs))

    # Get text and confidence from response
    text_annotation = response.full_text_annotation
    text = text_annotation.text
    confidence = 0
    if text_annotation.pages:
        confidence = text_annotation.pages[0].blocks[0].confidence * 100
    return text.strip(), confidence


def _get_random_temp_file_name(ext=''):
    # generate a random string of 5 characters
    fname = ''.join(
        choice(string.digits + string.ascii_letters) for _ in range(5))
    # generate a random temp file name
    return os.path.join(gettempdir(),
                        fname + os.extsep + ext if ext else fname)
