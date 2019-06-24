import pytest


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
