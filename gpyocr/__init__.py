"""
gpyocr - Python wrapper to Tesseract OCR and Google Vision OCR
"""


__version__ = "1.3"


from ._gpyocr import (
    SUPPORTED_FORMATS,
    get_tesseract_version,
    tesseract_ocr,
    get_google_vision_version,
    google_vision_ocr,
)
