# -*- coding: utf-8 -*-

"""
Top-level package for Will's Python Utilities.

Also includes some generic routines.

__init__.py
(c) Will Roberts  23 June, 2017
"""

from __future__ import absolute_import

from .io import lines, open_file as open   # noqa: F401
from .os import mkdir_p                    # noqa: F401

__author__ = """Will Roberts"""
__email__ = 'wildwilhelm@gmail.com'
__version__ = '1.0.0'


def memoize(func):
    """
    Memoization decorator for functions taking one or more arguments.

    This decorator works only with positional arguments, not with
    keyword arguments.

    Taken from:

    http://code.activestate.com/recipes/
        578231-probably-the-fastest-memoization-decorator-in-the-/
    """
    class MemoDict(dict):
        def __init__(self, func):
            self.func = func

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.func(*key)
            return ret
    return MemoDict(func)


def reduce_lists(lists):
    """
    Compute the list reduction of a list of iterables.

    Equivalent to (though faster than)::

        reduce(lambda a, b: a + b, lists, [])
    """
    retval = []
    for item in lists:
        retval.extend(item)
    return retval


def reduce_sets_or(sets):
    """
    Compute the set conjunctive reduction of a list of iterables.

    Equivalent to (though faster than)::

        reduce(lambda a, b: a | b, sets, set())
    """
    retval = set()
    for item in sets:
        retval.update(item)
    return retval
