# -*- coding: utf-8 -*-

"""
Pandas-related routines.

pd.py
(c) Will Roberts  23 June, 2017
"""

from __future__ import absolute_import

import collections

import pandas as pd


def pandas_memoize_csv(csv_filename, **kwds):
    """
    Memoize the pandas DataFrame result of a function to a CSV file.

    :param str csv_filename:
    :param dict kwds: passed to the pd.read_csv function
    """

    def pandas_memoize_csv_decorator(func):
        def func_wrapper(*args, **kwargs):
            try:
                retval = pd.read_csv(
                    csv_filename, encoding="utf-8", index_col=0, **kwds
                )
            except IOError:
                retval = func(*args, **kwargs)
                retval.to_csv(csv_filename, encoding="utf-8")
            return retval

        return func_wrapper

    return pandas_memoize_csv_decorator


# based on
# https://stackoverflow.com/a/62186053
def flatten_dict(dictionary, parent_key=False, separator="."):
    """
    Turn a nested dictionary into a flattened dictionary
    :param dictionary: The dictionary to flatten
    :param parent_key: The string to prepend to dictionary's keys
    :param separator: The string used to separate flattened keys
    :return: A flattened dictionary
    """

    items = []
    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key
        if isinstance(value, collections.abc.MutableMapping):
            items.extend(flatten_dict(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten_dict({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


class AutoExpandingDict(collections.defaultdict):
    def __init__(self, /, *args, **kwargs):
        super().__init__(self.__class__, *args, **kwargs)


def _intkeys_to_lists(dictionary):
    if not isinstance(dictionary, collections.abc.MutableMapping):
        return dictionary
    # bottom-up tree traversal
    result = {key: _intkeys_to_lists(dictionary[key]) for key in dictionary}
    if all(key.isdigit() for key in result.keys()) and set(result.keys()) == {
        str(idx) for idx in range(len(result))
    }:
        return [result[str(idx)] for idx in range(len(result))]
    else:
        return result


def unflatten_dict(dictionary, separator=".", intkeys_to_lists=True):
    result = AutoExpandingDict()
    for key, value in dictionary.items():
        path = key.split(separator)
        ptr = result
        for part in path[:-1]:
            ptr = ptr[part]
        ptr[path[-1]] = value
    if intkeys_to_lists:
        result = _intkeys_to_lists(result)
    return result


def unflatten_pd_row(row, prefix="", separator=".", intkeys_to_lists=True):
    columns = [c for c in row.index if c.startswith(prefix)]
    result = unflatten_dict(
        row[columns].to_dict(), separator=separator, intkeys_to_lists=False
    )
    if prefix and prefix.strip():
        path = prefix.split(".")
        for part in path:
            result = result[part]
    if intkeys_to_lists:
        result = _intkeys_to_lists(result)
    return result
