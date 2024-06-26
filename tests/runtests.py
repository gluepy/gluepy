#!/usr/bin/env python
"""Entrypoint for test suite that auto load settings and dependencies"""
import logging
import os
import sys
import unittest


def set_envs():
    os.environ["GLUEPY_SETTINGS_MODULE"] = "settings"


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(".")

    # Set log level for all logs during tests.
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(logging.ERROR)

    set_envs()
    runner = unittest.TextTestRunner()
    res = runner.run(suite)
    sys.exit(0 if res.wasSuccessful() else 1)
