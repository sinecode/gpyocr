import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "tesseract: Tesseract tests")
    config.addinivalue_line(
        "markers", "googlevision: Google Cloud Vision tests"
    )


def pytest_addoption(parser):
    parser.addoption(
        "--nomock",
        action="store_true",
        help="run tests without mocking the OCR engines",
    )


def pytest_generate_tests(metafunc):
    ConfTest.nomock = metafunc.config.getoption("--nomock")


class ConfTest:
    nomock = False
