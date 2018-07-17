'''
This module contains the main method to perform OCR from command line
'''


import argparse
from time import time

import pyocr


def main():
    parser = argparse.ArgumentParser(
        description='Process OCR with Tesseract or Google Vision OCR')
    parser.add_argument(dest='ocrengine',
                        choices={'tesseract', 'google-vision'},
                        help='OCR engine to use')
    parser.add_argument(dest='filepath', action='store',
                        help='path to the image where to perform OCR')
    parser.add_argument('-v', '--version', action='version',
                        version='pyocr {}'.format(pyocr.__version__),
                        help='print the current version of pyocr')

    args = parser.parse_args()

    start_time = time()
    if args.ocrengine == 'tesseract':
        text, conf = pyocr.tesseract_ocr(args.filepath)
    elif args.ocrengine == 'google-vision':
        print 'OCR with google-vision'
        return
    else:
        pass  # should not be there
    end_time = time()

    print 'OCR result'.center(50, '=')
    print text
    print ''.center(50, '=')
    print 'Info'.center(50, '=')
    print 'Confidence: {:.2f}%'.format(conf)
    print 'OCR engine: {}'.format(args.ocrengine)
    print 'Elapsed time: {:.3f} seconds'.format(end_time - start_time)
    print ''.center(50, '=')



if __name__ == '__main__':
    main()
