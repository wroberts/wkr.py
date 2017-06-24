# -*- coding: utf-8 -*-

"""
Pandas-related routines.

pd.py
(c) Will Roberts  23 June, 2017
"""

from __future__ import absolute_import

import pandas as pd


def pandas_memoize(csv_filename):
    """
    Decorator.

    Memoize the pandas DataFrame result of the given function to the
    named CSV file.
    """
    def pandas_memoize_decorator(func):
        def func_wrapper(*args, **kwargs):
            try:
                retval = pd.read_csv(csv_filename,
                                     encoding='utf-8', index_col=0)
            except IOError:
                retval = func(*args, **kwargs)
                retval.to_csv(csv_filename, encoding='utf-8')
            return retval
        return func_wrapper
    return pandas_memoize_decorator
