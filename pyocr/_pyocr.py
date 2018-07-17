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


__all__ = ('tesseract_ocr')


SUPPORTED_FORMATS = ('.gif', '.png', '.jpg', '.jpeg', '.tif', '.tiff')


def tesseract_ocr(image, lang='', psm=None, config=''):
    '''Execute a Tesseract call

    Return the text recognized with Tesseract OCR and a confidence
    value of the result. It needs Tesseract >= 3.05
    The image parameter could be:
        - a path to the image file
        - a numpy object (OpenCV)
        - an Image object (Pillow/PIL)
    '''
    image_path = _save_image(image)
    output_path = _get_random_temp_file_name()

    # build Tesseract command
    tesseract_cmd = ['tesseract', image_path, output_path]
    if lang:
        tesseract_cmd.append('-l {}'.format(lang))
    if psm:
        tesseract_cmd.append('--psm={}'.format(psm))
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
            c = int(row['conf'])
            if c > 0:
                text_line.append(row['text'])
                conf += c
                conf_num += 1
            else:
                text.append(' '.join(c for c in text_line))
                text_line = []
    if conf_num > 0:
        conf = int(conf / conf_num)

    # remove the two temporary files: image and output file
    if not isinstance(image, str):
        os.remove(image_path)
    os.remove(output_path)

    # return the tuple (text, confidence)
    return '\n'.join(line for line in text).strip(), conf


def _save_image(image):
    # check if it's a valid image path
    if isinstance(image, str):
        __, ext = os.path.splitext(image)
        if ext.lower() not in SUPPORTED_FORMATS:
            raise Exception('{} is not a valid image'.format(image))
        return image

    file_name = _get_random_temp_file_name(ext='jpg')
    # save the Numpy image
    if isinstance(image, np.ndarray):
        cv2.imwrite(file_name, image)
    # save the PIL image
    elif isinstance(image, Image.Image):
        if not image.mode.startswith('RGB'):
            image = image.convert('RGB')
        image.save(file_name)
    else:
        raise TypeError('The image could be a string containing the '
                        'path to the file, it could be a numpy '
                        'object or an Image PIL object')
    return file_name


def _get_random_temp_file_name(ext=''):
    # generate a random string of 5 characters
    fname = ''.join(
        choice(string.digits + string.ascii_letters) for _ in xrange(5))
    # generate a random temp file name
    return os.path.join(gettempdir(),
                        fname + os.extsep + ext if ext else fname)
