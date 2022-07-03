"""
gpyocr - Python wrapper to Tesseract OCR and Google Vision OCR
"""


__version__ = "1.5"


from ._gpyocr import (
    SUPPORTED_FORMATS,
    get_google_vision_version,
    get_tesseract_version,
    google_vision_ocr,
    tesseract_ocr,
)
