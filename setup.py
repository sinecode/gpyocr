from setuptools import setup

from pyocr import __version__

setup(
    name='pyocr',
    version=__version__,
    description='Python wrapper to Tesseract OCR and Google Vision OCR',
    url='https://github.com/check-emee/pyocr',
    author='Emilio Cecchini',
    author_email='cecchini.mle@gmail.com',
    keywords='OCR tesseract google vision wrapper',
    classifiers=[
        'Operating System :: Linux',
        'Programming Language :: Python :: 2.7'
    ],
    packages=[
        'pyocr'
    ],
    entry_points={
        'console_scripts': [
            'pyocr = pyocr.__main__:main'
        ]
    }
)
