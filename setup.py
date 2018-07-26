from setuptools import setup

from pygocr import __version__

setup(
    name='pygocr',
    version=__version__,
    description='Python wrapper for Tesseract OCR and Google Vision OCR',
    url='https://github.com/check-emee/pygocr',
    author='Emilio Cecchini',
    author_email='cecchini.mle@gmail.com',
    keywords='OCR tesseract google vision wrapper',
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    packages=[
        'pygocr'
    ],
    entry_points={
        'console_scripts': [
            'pygocr = pygocr.__main__:main'
        ]
    }
)
