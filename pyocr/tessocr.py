'''
Module to wrap Tesseract OCR
'''


def tesseract_ocr(image, lang='', psm=3, whitelist=''):
    '''Execute a Tesseract call

    Return the text recognized with Tesseract OCR and a confidence
    value of the result.
    The image parameter could be:
        - a path to the image file
        - a numpy object (OpenCV)
        - an Image object (Pillow/PIL)
    '''
    return
