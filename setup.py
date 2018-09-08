from setuptools import setup, find_packages

from gpyocr import __version__


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='Gpyocr',
    version=__version__,
    description='Python wrapper for Tesseract OCR and Google Vision OCR',
    long_description=long_description,
    url='https://github.com/check-emee/gpyocr',
    author='Emilio Cecchini',
    author_email='cecchini.mle@gmail.com',
    keywords='OCR tesseract google vision wrapper',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'gpyocr = gpyocr.__main__:main'
        ]
    },
    license='Apache 2.0',
    install_requires=[
        'opencv-python',
        'Pillow',
        'google-cloud-vision'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ]
)
