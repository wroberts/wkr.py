# -*- coding: utf-8 -*-

"""
OS-level routines.

os.py
(c) Will Roberts  23 June, 2017
"""

from __future__ import absolute_import

import errno
import os


def mkdir_p(path):
    """Functionality similar to mkdir -p."""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
