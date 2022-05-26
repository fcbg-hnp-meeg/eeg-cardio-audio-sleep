"""Eye-link module."""

from .. import logger
from .._typing import EYELink
from ..utils._imports import import_optional_dependency


class EyelinkMock(EYELink):
    def __init__(self, pname=None, fname=None, host_ip=None):
        logger.info("Eye-tracker: creating a MOCK eye-tracker.")
        self.el_tracker = _ElTrackerMock()

    def calibrate(self):
        logger.info("Eye-tracker: mock calibration.")

    def start(self):
        logger.info("Eye-tracker: mock start.")

    def stop(self):
        logger.info("Eye-tracker: mock stop.")


class _ElTrackerMock:
    def __init__(self):
        pass

    def sendMessage(self, value: str):
        logger.info("Eye-tracker: mock trigger %s.", value)


pylink = import_optional_dependency("pylink", raise_error=False)
if pylink is None:
    logger.error(
        "The pylink library could not be found! Eye-tracking will " "not work."
    )
    Eyelink = EyelinkMock
else:
    from .EyeLink import Eyelink  # noqa: F401